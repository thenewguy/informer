'use strict';

describe('Checker', function () {

    beforeEach(module('InformerApp'));

    describe('Details Controller', function () {
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

        it('when a registered Informer is called, details must be shown', function () {
            var response = {
                'operational': true,
                'name': 'DatabaseInformer',
                'message': 'your database is operational'
            }

            httpBackend.expectGET('/database').respond(response);

            controller('DetailController', {
                $scope: scope,
                $routeParams: { 'informer': 'database'}
            });

            httpBackend.flush();

            var result = angular.equals(scope.informer, response);

            expect(true).toEqual(result);
        });

        it('when a unexpected error occurs on backend, the message must be corrected', function () {
            httpBackend.expectGET('/database').respond(500);

            controller('DetailController', {
                $scope: scope,
                $routeParams: { 'informer': 'database'}
            });

            httpBackend.flush();

            expect(scope.informer).toEqual({});
            expect(scope.message).toBe('Crap. A error ocurred.');
        });
  });
});