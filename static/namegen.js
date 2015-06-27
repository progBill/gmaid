angular.module('gmAid',[])
  .controller('townCrafter', function($scope, $http){
      var npcGen = this;
      $scope.npcGen = {};
      $scope.npcGen.getName = function(item, event){
          // call to server for name
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
          var townResponse = $http.get("/gettown");
          townResponse.success(
              function(data, status, headers, config){
                  $scope.townResponse = data.name;
              });
          townResponse.error(
              function(data, status, headers, config){
                  $scope.townResponse = "Error getting town name";
              });
          var numDudes = $scope.numDudes;
          var npcResponse = $http.post("/getname/" + $scope.numDudes, {cultureFilter: $scope.npcGen.cultureFilter});
          npcResponse.success(function(data, status, headers, config){
              $scope.npcGen.nameResponse = data;
          });
          npcResponse.error(function(){
              $scope.npcGen.nameResponse = "Didn't work out";
          });
      }
      // dealing with a select box
      $scope.npcGen.villageSize = [
          {id:0, name:'Choose a settlement'},
          {id:1, name:'Village'},
          {id:2, name:'Town'},
          {id:3, name:'City'},
          {id:4, name:'Big City'}
      ];
      // set a default option
      $scope.npcGen.selectedItem = $scope.npcGen.villageSize[0];
      // set value when selectbox option is selected
      $scope.npcGen.onchange = function(id){
          $scope.numDudes = id.id * 10;
      };
});
