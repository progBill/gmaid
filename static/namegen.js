
// THE APP ITSELF
var townGen = angular.module('gmAid',[]);

//  CONTROLLERS
  townGen.controller('townCrafter', ['$scope','$http','townService', function($scope, $http, town){
      var npcGen = this;
      $scope.npcGen = {};
      $scope.npcGen.getTown = function(item, event){
          var townResponse = $http.post("/gettown/" + $scope.numDudes,
          {
            "cultureFilter": $scope.npcGen.cultureFilter,
            "size": $scope.numDudes,
          });
          townResponse.success(
              function(data, status, headers, config){
                  $scope.townName = data.name;
                  $scope.buildings= data.buildings;
                  $scope.nameResponse = data.npcs;
              });
          townResponse.error(
              function(data, status, headers, config){
                  $scope.townName = "Error getting town name";
                  $scope.buildings = false;
                  $scope.nameResponse = false;
              });
      };

      // dealing with a select box
      $scope.npcGen.villageSize = [
          {id:0, name:'Choose a settlement'},
          {id:100, name:'Village'},
          {id:200, name:'Town'},
          {id:300, name:'City'},
          {id:400, name:'Big City'},
      ];
      // set a default option for the selectbox
      $scope.npcGen.selectedItem = $scope.npcGen.villageSize[0];
      // set value when selectbox option is selected
      $scope.npcGen.onchange = function(id){ // TODO: I'm betting this means only 1 select box possible
          $scope.numDudes = id.id;
      };
}]);


// DIRECTIVES


// SERVICES
townGen.service('townService',function($http){
  return
  $http.post("/gettown/" + numDudes,
  {
    "cultureFilter": cultureFilter,
    "size": villageSize,
  })
  .success(
      function(data, status, headers, config){
          $scope.townName = data.name;
          $scope.buildings= data.buildings;
          $scope.nameResponse = data.npcs;
      })
  .error(
      function(data, status, headers, config){
          $scope.townName = "Error getting town name";
          $scope.buildings = false;
          $scope.nameResponse = false;
      });
});
