(function () {
    'use strict';

    var checker = angular.module('informer.checker', ['ngResource']);

    checker.controller('DetailController', ['$scope', '$routeParams', 'InformerService', 'MeasureService', DetailController]);

    function DetailController ($scope, params, Informer, Measure) {
        $scope.informer = {};
        $scope.availability = 0;

        Informer.get({ 'informer': params.informer }, successOnGetInformerDetails, fail);

        function successOnGetInformerDetails (response) {
            $scope.informer = response;

            angular.forEach(response.measures, function (value, key) {
                Measure.query({ 'informer': params.informer, 'measure': value }, successOnGetMeasureDetails, fail);
            }, null);

            function successOnGetMeasureDetails (response) {
                var online = 0;

                angular.forEach(response, function (raw) {
                    if (raw.value) {
                        online += 1;
                    }

                    $scope.availability = (100 * online) / response.length;
                }, online);
            }

        }

        function fail () {
            $scope.informer = {};
            $scope.message = 'Crap. A error ocurred.';
        }
    }
})();
