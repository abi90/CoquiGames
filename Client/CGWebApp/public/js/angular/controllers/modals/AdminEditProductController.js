/**
 * Created by jesmarie on 12-04-16.
 */
/**
 * Created by abi on 12/1/16.
 */
app.controller('AdmingEditProductController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'product',
    'adminwsapi', 'Upload', 'cloudinary',
    function ($scope, authenticationSvc, $rootScope, Popeye, product, adminwsapi, $upload, cloudinary){

        $scope.auth = authenticationSvc.getUserInfo();

        $scope.selectedProduct = {};

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



        var setProduct = function () {
            var tempProduct = {
                "availability": product.availability,
                "aditionalinfo": product.aditionalinfo,
                "category": product.category,
                "description": product.description,
                "esrb": product.esrb,
                "genre": product.genre,
                "inoffer": product.inoffer,
                "offerprice": product.offerprice,
                "photolink": product.photolink,
                "pid": product.pid,
                "platformid": product.platformid,
                "price": product.price,
                "rating": product.rating,
                "release": product.release,
                "title": product.title,
                "productqty": product.productqty,
                "offer_start_date": product.offer_start_date,
                "offer_end_date": product.offer_end_date,
                "active": product.active,
                "offerid": product.offerid
            };

            if(!product.inoffer){
                tempProduct.offerid=0;
                tempProduct.offer_start_date='';
                tempProduct.offer_end_date='';
            }

            $scope.selectedProduct = tempProduct;
        };

        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.submit = function() {
            return Popeye.closeCurrentModal($scope.selectedProduct);
        };

        $scope.cancel = function () {
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
                        $scope.selectedProduct.photolink = file.result.secure_url;
                        // Transform image link
                        $scope.selectedProduct.photolink = $scope.selectedProduct.photolink.replace('upload/','upload/c_pad,h_320,w_250/');
                        $rootScope.photos.push(data);
                    }).error(function (data, status, headers, config) {
                        file.result = data;
                    });
                }
            });
        };
        setProduct();


    }]);