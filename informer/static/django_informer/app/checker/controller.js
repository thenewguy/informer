(function () {
    'use strict';

    var checker = angular.module('informer.checker', ['ngResource']);

    checker.controller('DetailController', ['$scope', '$routeParams', 'InformerService', 'MeasureService', DetailController]);

    function DetailController ($scope, params, Informer, Measure) {
        $scope.informer = {};
        $scope.measures = [];

        Informer.get({ 'informer': params.informer }, successOnGetInformerDetails, fail);

        function successOnGetInformerDetails (response) {
            $scope.informer = response;

            angular.forEach(response.measures, function (value, key) {
                Measure.query({ 'informer': params.informer, 'measure': value }, successOnGetMeasureDetails, fail);
            }, null);

            function successOnGetMeasureDetails (response) {
                angular.forEach(response, function (raw) {
                    this.push(raw);
                }, $scope.measures);
            }

        }

        function fail () {
            $scope.informer = {};
            $scope.message = 'Crap. A error ocurred.';
        }
    }
})();
