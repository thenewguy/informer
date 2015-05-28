(function () {
    'use strict';

    var home = angular.module('Home', ['ngResource']);

    home.controller('DashboardController', ['$scope', 'InformerDiscoverService', 'InformerService', DashboardController]);
    
    function DashboardController ($scope, Discover, Informer) {
        $scope.informers = [];
        $scope.message = 'All systems operational.';

        var informers = Discover.query({}, successOnGetInformersList, fail);

        function successOnGetInformersList (response) {
            angular.forEach(response.informers, function (item) {
                Informer.get({ 'informer': item.name }, successOnGetInformerDetails);
            });
        }

        function successOnGetInformerDetails (response) {
            if (!response.operational) {
                $scope.message = 'Oh my god. Something goes wrong.';
            }

            $scope.informers.push(response);
        }

        function fail () {
            $scope.message = 'Crap. A error ocurred.';
        }
    }

})();
