(function () {
  'use strict';

  angular
      .module('horizon.dashboard.admin.venus')
      .controller('LogSearchController', LogSearchController);

  LogSearchController.$inject = ['$scope', 'venusSrv'];

  function LogSearchController($scope, venusSrv) {
    $scope.STATIC_URL = STATIC_URL;
    $scope.model = {
      start_time: new Date(),
      end_time: new Date(),
      condition: 'module_name',
      page_size: horizon.cookies.get('API_RESULT_PAGE_SIZE') || 20,
      page_num: 1
    };
    $scope.total = 0;
    $scope.tableData = [];
    $scope.chartsData = []; // 数据形如：{key_as_string: '2022-05-30T15:30:00.000+08:00', doc_count: 20}

    $scope.getData = function () {
      var config = {
        start_time: $scope.model.start_time.getTime() / 1000,
        end_time: $scope.model.end_time.getTime() / 1000,
        page_size: $scope.model.page_size,
        page_num: $scope.model.page_num
      };
      venusSrv.getLogs(config).then(function (res) {
        $scope.tableData = [];
        if (res.data.hasOwnProperty('data')) {
          $scope.tableData = res.data.data.values;
          $scope.chartsData = res.data.data_stats.count;
          $scope.total = res.data.data.total;
        }
        $scope.updateCharts();
      });
    };

    $scope.updateCharts = function () {
      var svg = d3.select('#svg');

      var width = svg.node().getBoundingClientRect().width,
          height = svg.node().getBoundingClientRect().height,
          barHotZoneWidth = width / $scope.chartsData.length,
          barHotZoneHighlight = '#ff0000',
          barWidth = barHotZoneWidth - 2,
          barBgColor = '#007ede';

      var xScale = d3.scale.linear()
          .domain([0, $scope.chartsData.length - 1])
          .range([0, width]);

      var hScale = d3.scale.linear()
          .domain(d3.extent($scope.chartsData, d => d.doc_count))
          .range([0, height]);

      var bars = svg.selectAll('g')
          .data($scope.chartsData);

      var yAxis = d3.svg.axis()
          .scale(hScale)
          .orient('left');

      svg.select('#yAxis')
          .remove();

      svg.append('g')
          .attr('id', 'yAxis')
          .attr('transform', 'translate(30,0)')
          .call(yAxis);

      // enter
      bars.enter()
          .append('g')
          .append('rect')
          .attr('fill', barBgColor)
          .attr('x', (d, i) => xScale(i))
          .attr('y', (d) => height - hScale(d.doc_count))
          .attr('width', barWidth)
          .attr('height', (d) => hScale(d.doc_count));

      // update
      bars.select('rect')
          .attr('x', (d, i) => xScale(i))
          .attr('y', (d) => height - hScale(d.doc_count))
          .attr('width', barWidth)
          .attr('height', (d) => hScale(d.doc_count));

      // exit
      bars.exit()
          .remove();
    };

    function init() {
      var end_time = new Date();
      end_time.setMilliseconds(0);
      var start_time = new Date();
      start_time.setMilliseconds(0);
      start_time.setTime(end_time.getTime() - 24 * 60 * 60 * 1000);
      $scope.model.start_time = start_time;
      $scope.model.end_time = end_time;

      $scope.getData();
    }

    init();
  }

})();
