/**
 * Created by jesmarie on 12-05-16.
 */
app.controller('AdminAddProductController',
    ['$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'adminwsapi', 'Upload', 'cloudinary',
    function ($scope, authenticationSvc, $rootScope, Popeye, adminwsapi, $upload, cloudinary){

        $scope.auth = authenticationSvc.getUserInfo();

        adminwsapi.getESRBRating($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.ratings = response.data
            },
            function () {
                $scope.ratings = [];
            }
        );

        adminwsapi.getCategories($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.categories = response.data
            },
            function () {
                $scope.categories = [];
            }
        );

        adminwsapi.getPlatforms($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.platforms = response.data
            },
            function () {
                $scope.platforms = [];
            }
        );

        adminwsapi.getGenres($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.genres = response.data
            },
            function () {
                $scope.genres = [];
            }
        );

        $scope.patterns={
            bigText: '[a-zA-Z\\d\\.\\:\\,\\;\\s\\-\\!\\?\\>\\<\\&\\^\\%\\$\\#\\@\\*\\(\\)\\_\\=\\`\\~\\/\\\]+',
            date: /\d{4}-\d{2}-\d{2}/,
            url: '((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?'
        };

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

        $scope.uploadFiles = function(files){
            $scope.files = files;
            if (!$scope.files) return;
            angular.forEach(files, function(file){
                if (file && !file.$error) {
                    file.upload = $upload.upload({
                        url: "https://api.cloudinary.com/v1_1/" + cloudinary.config().cloud_name + "/upload",
                        data: {
                            upload_preset: cloudinary.config().upload_preset,
                            tags: 'product',
                            context: 'photo=' + $scope.selectedProduct.title,
                            file: file
                        }
                    }).progress(function (e) {
                        file.progress = Math.round((e.loaded * 100.0) / e.total);
                        file.status = "Uploading... " + file.progress + "%";
                    }).success(function (data, status, headers, config) {
                        data.context = {custom: {photo: $scope.selectedProduct.title}};
                        file.result = data;
                        $scope.selectedProduct.photolink = file.result.secure_url;
                        // Transform image link
                        $scope.selectedProduct.photolink = $scope.selectedProduct.photolink.replace('upload/','upload/c_pad,h_320,w_250/');
                    }).error(function (data, status, headers, config) {
                        file.result = data;
                    });
                }
            });
        };


    }]);