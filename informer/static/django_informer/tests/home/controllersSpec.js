'use strict';

describe('Home', function () {

    beforeEach(module('InformerApp'));

    describe('Dashboard Controller', function () {
        var scope, controller, httpBackend;

        beforeEach(inject(function($rootScope, $controller, $httpBackend) {
            scope = $rootScope.$new();
            controller = $controller;
            httpBackend = $httpBackend;
        }));

        afterEach(function() {
            httpBackend.verifyNoOutstandingExpectation();
            httpBackend.verifyNoOutstandingRequest();
        });

        it('should have "informers" and their results fetched from xhr', function () {

            httpBackend.expectGET('/discover').respond({
                'informers': [{
                    'name': 'database',
                    'url': '/database/'
                }]
            });

            httpBackend.expectGET('/database').respond({
                'operational': true,
                'name': 'DatabaseInformer',
                'message': 'your database is operational'
            });

            controller('DashboardController', {
                $scope: scope
            });

            httpBackend.flush();

            expect(1).toBe(scope.informers.length);
            expect(scope.message).toBe('All systems are operational.');
        });

        it('when the Informer detect a fail, the message must be corrected', function () {

            httpBackend.expectGET('/discover').respond({
                'informers': [{
                    'name': 'database',
                    'url': '/database/'
                }, {
                    'name': 'blah',
                    'url': '/blah/'
                }]
            });

            httpBackend.expectGET('/database').respond({
                'operational': true,
                'name': 'DatabaseInformer',
                'message': 'your database is operational'
            });

            httpBackend.expectGET('/blah').respond({
                'operational': false,
                'name': 'BlahInformer',
                'message': 'a message with bad news'
            });

            controller('DashboardController', {
                $scope: scope
            });

            httpBackend.flush();

            expect(2).toBe(scope.informers.length);
            expect(scope.message).toBe('Oh my god. Something goes wrong.');
        });

        it('when a unexpected error occurs on backend, the message must be corrected', function () {

            httpBackend.expectGET('/discover').respond(500);

            controller('DashboardController', {
                $scope: scope
            });

            httpBackend.flush();

            expect(scope.message).toBe('Crap. A error ocurred.');
        });
  });
});


describe('Filters', function () {
    beforeEach(module('InformerApp'));

    describe('name', function () {
        var filter;

        beforeEach(inject(function(nameFilter) {
            filter = nameFilter;
        }));

        it('should remove prefix or suffix from Informer name', function () {
            expect(filter('InformerDatabase')).toBe('database');
        });
    });
});
