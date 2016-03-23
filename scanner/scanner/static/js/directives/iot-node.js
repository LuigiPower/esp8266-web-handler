(function(){
    "use strict";

    var app = angular.module("iot-module");

    app.directive("iotNode", function() {
        return {
            controller: "IotNodeController",
            templateUrl: "templates/iot-node-template.html",
            restrict: "E",
            scope: {
                node_data: "="
            }
        };
    });
})();
