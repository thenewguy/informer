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

            Measure.query({'informer': params.informer, 'measure': 'availability' }, calculateAvailability, fail);
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
