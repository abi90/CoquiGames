/**
 * Created by abi on 11/12/16.
 */
app.controller("SearchController", ["$scope", "$location", "storewsapi", "title", '$rootScope',
    function ($scope, $location, storewsapi, title, $rootScope) {
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
        $scope.qty = {max: 9};
        $scope.propertyName = 'Title';
        $scope.format = false;
        $scope.platformSelection = -1;
        $scope.priceRangeSelection = {from: -1, to: -1};


        $scope.orderByFunc = function(product){
            if($scope.propertyName == 'highest'){
                $scope.format = true;
                return parseFloat(product.price);
            }
            else if($scope.propertyName == 'lowest'){
                $scope.format = false;
                return parseFloat(product.price);
            }
            else if($scope.propertyName == 'A-Z')
            {
                $scope.format = false;
                return product.title;
            }
            else if($scope.propertyName == 'Z-A')
            {
                $scope.format = true;
                return product.title;
            }
            else if($scope.propertyName == 'Title')
            {
                $scope.format = false;
                return product.title;
            }
            if($scope.propertyName == 'Price'){
                $scope.format = false;
                return parseFloat(product.price);
            }

        };

        //Local functions
        var searchByTitle = function (title) {
            if(title.length > 0){
                storewsapi.searchByTitle(title).then(
                    function (response) {
                        $scope.results = response.data
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

        $scope.filterAction = function () {
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
                        $scope.results = response.data
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


        //Get Results on startup
        searchByTitle(title);
        getGenres();

    }]);