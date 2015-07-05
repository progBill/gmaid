
// THE APP ITSELF
var townGen = angular.module('gmAid',[]);

//  CONTROLLERS
  townGen.controller('townCrafter', ['$scope','$http','townService', function($scope, $http, town){
      var npcGen = this;
      $scope.npcGen = {};

      $scope.npcGen.getTown = function(){

        $scope.townName = null;
        $scope.buildings= null;
        $scope.nameResponse = null;

        town.getTown( $scope.numDudes, $scope.npcGen.cultureFilter )
        .then(function( d ){

          $scope.townName = d.name;
          $scope.buildings= d.buildings;
          $scope.nameResponse = d.npcs;
        },function(e){ console.log(e); });
      };

}]);

/////////////
// FILTERS //
/////////////

  //stolen from SO: http://stackoverflow.com/questions/19387552/angular-cant-make-ng-repeat-orderby-work/19387871#19387871
townGen.filter('object2Array', function() {
    return function(input) {
      var out = [];
      for(i in input){
        out.push(input[i]);
      }
      return out;
    }
  });


// DIRECTIVES



//////////////
// SERVICES //
//////////////


// stolen almost completely wholesale from: http://www.bennadel.com/blog/2612-using-the-http-service-in-angularjs-to-make-ajax-requests.htm
townGen.service('townService',
function($http, $q){
  // public API
  return({
    getTown: getTown
  });

  function getTown(numDudes, cultureFilter){
    var req = $http({
      method: "post",
      url: "/gettown/" + numDudes,
      data:{"cultureFilter": cultureFilter,"size": numDudes},
    });

    return( req.then(handleSuccess, handleError) );

  }

  //
  //  PRIVATE METHODS
  //

  function handleError( response ) {

      if (
          ! angular.isObject( response.data ) ||
          ! response.data.message
          ) {
          return( $q.reject( "An unknown error occurred." ) );
      }
      return( $q.reject( response.data.message ) );
  }

  function handleSuccess( response ) {
    return( response.data );
  }

});
