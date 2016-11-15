/**
 * Created by abi on 11/12/16.
 */
app.controller("SearchController", ["$scope", "$location", "storewsapi", "title", '$rootScope', 'Popeye', 'orderByFilter',
    function ($scope, $location, storewsapi, title, $rootScope, Popeye, orderBy) {
        //Scope Variables
        $scope.title = title;
        $scope.results = [];
        $scope.list = true;
        $scope.genres = [];
        $scope.priceRanges = [
            {from: 0, to: 9.99},
            {from: 10, to: 19.99},
            {from: 20, to: 29.99},
            {from: 30, to: 39.99},
            {from: 40, to: 99.99},
            {from: 100, to: 299.99},
            {from: 300, to: 9999.99}
        ];
        $scope.genresSelection = [];
        $scope.propertyName = {name: 'Title'};
        $scope.format = false;
        $scope.platformSelection = -1;
        $scope.priceRangeSelection = {from: -1, to: -1};
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
        var searchByTitle = function (title) {
            if(title.length > 0){
                storewsapi.searchByTitle(title).then(
                    function (response) {
                        $scope.results = response.data;
                        sliceResults();
                    },
                    function (error) {
                        console.log(error.toString());
                        $scope.results = [];
                    }
                );
            }
            else {
                //Empty Search
                $location.path("/index.html");
            }

        };

        var getGenres = function () {
            storewsapi.getGenres().then(
                function (response) {
                    $scope.genres = response.data;
                },
                function (error) {
                    console.log(response.data.toString());
                    $scope.genres = [];
                }
            )

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

        // toggle selection for a given genre by name
        $scope.toggleSelection = function toggleSelection(genre) {
            var idx = $scope.genresSelection.indexOf(genre);

            // is currently selected
            if (idx === -1) {
                $scope.genresSelection.push(genre);
            }

            // is newly selected
            else {
                $scope.genresSelection.splice(idx, 1);
            }
        };

        $scope.filterAction = function (){
            var data = {title: title};
            if($scope.priceRangeSelection.to > 0){
                data['price'] = $scope.priceRangeSelection;
            }
            if($scope.platformSelection > 0){
                data['platformid'] = $scope.platformSelection;
            }
            if($scope.genresSelection.length > 0){
                data['genres'] = $scope.genresSelection;
            }
            console.log(data)
            storewsapi.search(data).then(
                    function (response) {
                        $scope.results = response.data;
                        sliceResults();
                    },
                    function (error) {
                        console.log(error.toString());
                        $scope.results = [];
                    }
                );
        };

        $scope.selectPlatform = function(pid){
            $scope.platformSelection = pid;
        };

        $scope.selectPriceRange = function(p){
            $scope.priceRangeSelection = p;
        };

        $scope.updateFilter = function () {
            sliceResults();
        };

        $scope.$watch("currentPage.number + qty.max", function () {
            sliceResults();
        });



        //Get Results on startup
        searchByTitle(title);
        getGenres();

    }]);