(function () {
    'use strict';

    var checker = angular.module('informer.checker');

    checker.directive('informerChart', ['MeasureService', function (Measure) {
        return {
            restrict: 'A',
            templateUrl: '/static/django_informer/app/checker/chart.tmpl.html',
            scope: {
                name: '@',
                collect: '@'
            },
            link: function (scope, element, attrs) {
                var container = element[0],
                    result = JSON.parse(scope.collect);

                google.charts.load('current', {'packages':['corechart']});
                google.charts.setOnLoadCallback(drawChart);

                function drawChart () {
                    //var data = google.visualization.arrayToDataTable(result)
                    var data = google.visualization.arrayToDataTable([
                        ['Year', 'Sales', 'Expenses'],
                        ['2004',  1000,      400],
                        ['2005',  1170,      460],
                        ['2006',  660,       1120],
                        ['2007',  1030,      540]
                    ]);

                    var options = {
                        title: 'Company Performance',
                        curveType: 'function',
                        legend: { position: 'bottom' }
                    };

                    var chart = new google.visualization.LineChart(
                        document.getElementById('curve_chart'));

                    chart.draw(data, options);
                }

                function onFailure () {
                }
            }
        };
    }]);

})();
