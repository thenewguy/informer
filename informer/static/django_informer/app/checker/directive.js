(function () {
    'use strict';

    var checker = angular.module('informer.checker');

    checker.directive('informerChart', ['MeasureService', function (Measure) {
        return {
            restrict: 'A',
            templateUrl: '/static/django_informer/app/checker/chart.tmpl.html',
            link: function (scope, element, attrs) {
                var container = element[0];
                var chart = new google.visualization.Timeline(container);
                var dataTable = new google.visualization.DataTable();

                dataTable.addColumn({ type: 'string', id: 'President' });
                dataTable.addColumn({ type: 'date', id: 'Start' });
                dataTable.addColumn({ type: 'date', id: 'End' });

                function onSuccess (response) {

                    dataTable.addRows([
                        [ 'Washington', new Date(1789, 3, 30), new Date(1797, 2, 4) ],
                        [ 'Adams',      new Date(1797, 2, 4),  new Date(1801, 2, 4) ],
                        [ 'Jefferson',  new Date(1801, 2, 4),  new Date(1809, 2, 4) ],
                    ]);

                    chart.draw(dataTable);
                }

                function onFailure () {
                }
            }
        };
    }]);

})();
