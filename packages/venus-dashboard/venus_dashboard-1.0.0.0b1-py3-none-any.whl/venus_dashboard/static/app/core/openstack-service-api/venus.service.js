(function () {
  'use strict';

  angular
      .module('horizon.app.core.openstack-service-api')
      .factory('horizon.app.core.openstack-service-api.venus', venusAPI);

  venusAPI.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service'

  ];

  function venusAPI(apiService, toastService) {

    function getLogStorageDays() {
      var url = '/api/venus/log_storage_days';

      return apiService.get(url)
          .catch(function () {
            // toastService.add('error', gettext('Unable to fetch the venus log storage days.'));
          });
    }

    function getLogs(config) {
      config = config || {};
      var url = '/api/venus/logs';

      return apiService.get(url, config)
          .catch(function () {
            // toastService.add('error', gettext('Unable to fetch the venus logs.'));
          });
    }

    var service = {
      getLogStorageDays: getLogStorageDays,
      getLogs: getLogs
    };

    return service;
  }

}());
