(function () {
    'use strict';

    var checker = angular.module('informer.checker');

    checker.directive('informerPostgresSizeChart', ['MeasureService', 'CONFIGURATION', function (Measure, Configuration) {
        return {
            restrict: 'A',
            template: '',
            scope: {
                name: '@',
                size: '@'
            },
            link: function (scope, element, attrs) {
                google.charts.load('current', {'packages':['line']});
                google.charts.setOnLoadCallback(drawChart);

                var component = element[0],
                    options = {
                        chart: {
                            title: 'Database size',
                            subtitle: 'database size collect every ' + Configuration.INTERVAL + ' minutes'
                        }
                    },
                    size = JSON.parse(scope.size),
                    rows = [];

                size.map(function (item) {
                    var date = new Date(item.date),
                        value = parseInt(item.value),
                        row = [date, value];

                    rows.push(row);
                });

                function drawChart () {
                    var data = new google.visualization.DataTable(),
                        chart = new google.charts.Line(component);

                    data.addColumn('datetime', null);
                    data.addColumn('number', 'Size');
                    data.addRows(rows);

                    chart.draw(data, options);
                }

                function onFailure () {
                }
            }
        };
    }]);

})();
