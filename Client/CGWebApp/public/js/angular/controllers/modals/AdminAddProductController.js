/**
 * Created by jesmarie on 12-05-16.
 */
/**
 * Created by jesmarie on 12-04-16.
 */
/**
 * Created by abi on 12/1/16.
 */
app.controller('AdminAddProductController', [ '$scope', 'authenticationSvc',  '$rootScope',
    'Popeye', 'adminwsapi', 'Upload', 'cloudinary',
    function ($scope, authenticationSvc, $rootScope, Popeye, adminwsapi, $upload, cloudinary){

        $scope.auth = authenticationSvc.getUserInfo();

        adminwsapi.getESRBRating($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.ratings = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.ratings = [];
            }
        );

        adminwsapi.getCategories($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.categories = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.categories = [];
            }
        );

        adminwsapi.getPlatforms($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.platforms = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.platforms = [];
            }
        );

        adminwsapi.getGenres($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.genres = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.genres = [];
            }
        );


        var tempProduct = {
            "availability": false,
            "aditionalinfo": null,
            "category": null,
            "description": null,
            "esrb": null,
            "genre": null,
            "inoffer": false,
            "offerprice": null,
            "photolink": null,
            "pid": null,
            "platformid": null,
            "price": null,
            "rating": null,
            "release": null,
            "title": null,
            "productqty": 0,
            "offer_start_date": null,
            "offer_end_date": null,
            "active": false
        };


        $scope.selectedProduct = tempProduct;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.submit = function() {
            $scope.selectedProduct = tempProduct;
            return Popeye.closeCurrentModal($scope.selectedProduct);
        };

        $scope.cancel = function () {
            $scope.selectedProduct= tempProduct;
            return Popeye.closeCurrentModal(null);
        };
        var d = new Date();
        //$scope.$watch('files', function() {
        $scope.uploadFiles = function(files){
            $scope.files = files;
            if (!$scope.files) return;
            angular.forEach(files, function(file){
                if (file && !file.$error) {
                    file.upload = $upload.upload({
                        url: "https://api.cloudinary.com/v1_1/" + cloudinary.config().cloud_name + "/upload",
                        data: {
                            upload_preset: cloudinary.config().upload_preset,
                            tags: 'myphotoalbum',
                            context: 'photo=' + $scope.selectedProduct.title,
                            file: file
                        }
                    }).progress(function (e) {
                        file.progress = Math.round((e.loaded * 100.0) / e.total);
                        file.status = "Uploading... " + file.progress + "%";
                    }).success(function (data, status, headers, config) {
                        $rootScope.photos = $rootScope.photos || [];
                        data.context = {custom: {photo: $scope.selectedProduct.title}};
                        file.result = data;
                        $scope.selectedProduct.photolink = file.result.url;
                        $rootScope.photos.push(data);
                    }).error(function (data, status, headers, config) {
                        file.result = data;
                    });
                }
            });
        };
        //});

        /* Modify the look and fill of the dropzone when files are being dragged over it */
        $scope.dragOverClass = function($event) {
            var items = $event.dataTransfer.items;
            var hasFile = false;
            if (items != null) {
                for (var i = 0 ; i < items.length; i++) {
                    if (items[i].kind == 'file') {
                        hasFile = true;
                        break;
                    }
                }
            } else {
                hasFile = true;
            }
            return hasFile ? "dragover" : "dragover-err";
        };

    }]);