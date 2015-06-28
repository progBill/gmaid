angular.module('gmAid',[])
  .controller('townCrafter', function($scope, $http){
      var npcGen = this;
      $scope.npcGen = {};
      $scope.npcGen.getName = function(item, event){
          var responsePromise = $http.post("/getname", {"cultureFilter": $scope.npcGen.cultureFilter });
          responsePromise.success(
              function(data, status, headers, config){
                  $scope.npcGen.nameResponse = data;
          });
          responsePromise.error(
              function(data, status, headers, config){
                  $scope.npcGen.nameResponse = "Error, Try Again";
          })
      };
      $scope.npcGen.getTown = function(item, event){
          var townResponse = $http.post("/gettown/" + $scope.numDudes,
            {cultureFilter: $scope.npcGen.cultureFilter, size: $scope.npcGen.villageSize.value});
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
      }
      // dealing with a select box
      $scope.npcGen.villageSize = [
          {id:0, name:'Choose a settlement'},
          {id:10, name:'Village'},
          {id:20, name:'Town'},
          {id:30, name:'City'},
          {id:40, name:'Big City'}
      ];
      // set a default option
      $scope.npcGen.selectedItem = $scope.npcGen.villageSize[0];
      // set value when selectbox option is selected
      $scope.npcGen.onchange = function(id){
          $scope.numDudes = id.id;
      };
});
