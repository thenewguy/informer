(function () {
    'use strict';

    var checker = angular.module('informer.checker');

    checker.directive('informerTimeSeriesChart', ['MeasureService', 'CONFIGURATION', function (Measure, Configuration) {
        return {
            restrict: 'A',
            template: '',
            scope: {
                informer: '@',
                measure: '@'
            },
            link: function (scope, element, attrs) {
                var component = element[0],
                    chart = new google.charts.Line(component),
                    data = new google.visualization.DataTable(),
                    params = {
                        'informer': scope.informer,
                        'measure': scope.measure
                    };

                data.addColumn('datetime', null);
                data.addColumn('number', scope.measure)

                Measure.query(params, function (response) {
                    response.map(function (item) {
                        var date = new Date(item.date),
                            value = parseInt(item.value);

                        data.addRow([date, value]);
                    });

                    chart.draw(data);
                });

                function onFailure () {
                }
            }
        };
    }]);

})();
