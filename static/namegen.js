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
          var townResponse = $http.post("/gettown/" + $scope.numDudes, {"cultureFilter": $scope.npcGen.cultureFilter, "size": $scope.npcGen.selectedItem.id});
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
          {id:500, name:'Metropolis'}
      ];
      // set a default option for the selectbox
      $scope.npcGen.selectedItem = $scope.npcGen.villageSize[0];
      // set value when selectbox option is selected
      $scope.npcGen.onchange = function(id){ // TODO: I'm betting this means only 1 select box possible
          $scope.numDudes = id.id;
          console.log( $scope.numDudes );
      };
});
