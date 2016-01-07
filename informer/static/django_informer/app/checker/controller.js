(function () {
    'use strict';

    var checker = angular.module('informer.checker', ['ngResource']);

    checker.controller('DetailController', ['$scope', '$routeParams', 'InformerService', 'MeasureService', DetailController]);

    function DetailController ($scope, params, Informer, Measure) {
        $scope.informer = {};
        $scope.availability = 0;
        $scope.measures = [];

        Informer.get({'informer': params.informer}, successOnGetDetails, fail);

        function successOnGetDetails (response) {
            $scope.informer = response;
            $scope.informer.measures.map(getMeasureValues);
        }

        function getMeasureValues (measure) {
            Measure.query({
                'informer': params.informer,
                'measure': measure
            }, function (response) {

                if (measure === 'availability') {
                    calculateAvailability(response);
                } else {
                    var data = {
                        'measure': measure,
                        'result': response
                    }

                    $scope.measures.push(data);

                }

            }, fail);
        }

        function fail () {
            $scope.informer = {};
            $scope.message = 'Crap. A error ocurred.';
        }

        function calculateAvailability (data) {
            var online = 0;

            angular.forEach(data, function (raw) {
                var up = JSON.parse(raw.value.toLowerCase());
                if (up) online += 1;

                $scope.availability = (100 * online) / data.length;
            }, online);
        }
    }
})();
