(function(){
    "use strict";

    var app = angular.module('session-module');

    app.controller("IotNodeController", ['$scope', function($scope) {

        $scope.getNodeName()
        {
            return $scope.node_data.name;
        };

        $scope.getNodeIP()
        {
            return $scope.node_data.ip;
        };

    }]);

})();
