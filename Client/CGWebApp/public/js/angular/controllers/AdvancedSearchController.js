/**
 * Created by felix on 12/1/16.
 */

app.controller("AdvancedSearchController", ["$scope", "$location", "storewsapi", "search_data", '$rootScope', 'orderByFilter',
    function ($scope, $location, storewsapi, search_data, $rootScope, orderBy) {

        //Scope Variables
        $scope.data = search_data;
        $scope.results = [];
        $scope.list = true;
        $scope.propertyName = {name: 'Title'};
        $scope.format = false;
        $scope.currentPage = {number: 1};
        $scope.qty = {max: 9};
        
        $scope.orderByFunc = function(product){
            if($scope.propertyName.name == 'highest' || $scope.propertyName.name == 'lowest' || $scope.propertyName.name == 'Price'){
                if(product.inoffer){
                    return parseFloat(product.offerprice);
                }
                return parseFloat(product.price);
            }
            else if($scope.propertyName.name == 'A-Z' || $scope.propertyName.name == 'Z-A' || $scope.propertyName.name == 'Title')
            {
                return product.title;
            }

        };

        //Local functions
        var searchByData = function (data) {
            var isValid = data.category.length >0 && data.genre.length>0 && data.platformid > 0;
            if(isValid){
                storewsapi.adSearch(data).then(
                    function (response) {
                        $scope.results = response.data;
                        sliceResults();
                    },
                    function (error) {
                        console.log(JSON.stringify(error));
                        $scope.results = [];
                    }
                );
            }
            else {
                //Empty Search
                $location.path("/index.html");
            }

        };

        var sliceResults= function () {
            if($scope.propertyName.name == 'highest' || $scope.propertyName.name == 'Z-A' || $scope.propertyName.name == 'Price'){
                $scope.format = true;
            }
            else if($scope.propertyName.name == 'lowest' || $scope.propertyName.name == 'A-Z' || $scope.propertyName.name == 'Title'){
                $scope.format = false;
            }

            var begin = (($scope.currentPage.number-1)*$scope.qty.max);
            var end = begin + $scope.qty.max;
            $scope.results = orderBy($scope.results, $scope.orderByFunc, $scope.format);
            $scope.FilteredResults = $scope.results.slice(begin, end);

        };

        //Scope Functions
        $scope.gridView = function () {
            $scope.list = false;
        };

        $scope.listView = function () {
            $scope.list = true;
        };


        $scope.updateFilter = function () {
            sliceResults();
        };

        $scope.$watch("currentPage.number + qty.max", function () {
            sliceResults();
        });


        //Get Results on startup
        searchByData($scope.data);



}]);