/**
 * Created by Abisai on 11/29/16.
 */
app.controller('RegisterController',
    ['$rootScope', '$scope', '$location', '$filter','userwsapi', 'authenticationSvc',
    function ($rootScope, $scope, $location, $filter, userwsapi, authenticationSvc){
        $scope.new_user = {
            ufirstname: '', ulastname: '', uemail: '', uphone: '', udob: '', uname: '', upassword: '', upassword2: '',
            ushippingaddress: {
                astate: '', aaddress1: '', aaddress2: '', acity: '', acountry: 'USA', afullname: '', azip: ''
            },
            ubillingaddress: {
                astate: '', aaddress1: '', aaddress2: '', acity: '', acountry: 'USA', afullname: '', azip: ''
            },
            upayment: {
                cname: '', cnumber: '', cexpdate: '', cvc: '', ctype: ''}
        };
        $scope.paymentYear = '';
        $scope.paymentMonth = '';
        $scope.yearOptions = [];
        $scope.password2 = '';
        $scope.aggrement = false;
        $scope.isPosting = false;
        $scope.userDOB = new Date();
        $scope.userCard = {cardNumber: null, CVC: null};
        $scope.regexs = {
            ccard: /^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13})$/g,
            bigText: '[a-zA-Z\\d\\.\\:\\,\\;\\s\\-]+',
            email: /(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/g,
            phone: /^(\d{3})([-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})$/g,
            userName: '[a-zA-Z]+[\\da-zA-Z]+',
            password: '[a-zA-Z\\d]+',
            cvc: '\\d{3}',
            postal: '\\d{5,6}'
        };

        var getYears = function () {
            var i;
            for (i = 0; i < 20; i++) {
                $scope.yearOptions[i] = new Date().getFullYear() + i;
            }
        };

        var getCardType = function (cardNumber) {
            var result = '';
            // Specific Credit Cards Regex
            var aExp = /^3[47][0-9]{13}$/g;
            var visa = /^4[0-9]{12}(?:[0-9]{3})?$/g;
            var mCard = /^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$/g;
            // Matches a card number
            if(cardNumber.match($scope.regexs.ccard)){
                result = (cardNumber.match(visa)) ? (cardNumber.match(visa).length == 1) ? 'Visa':result:result;
                result = (cardNumber.match(aExp)) ? (cardNumber.match(aExp).length == 1) ? 'American Express':result:result;
                result = (cardNumber.match(mCard)) ? (cardNumber.match(visa).length == 1) ? 'Master Card':result:result;
            }
            return result;
        };

        $scope.validPassword = function (){
            return angular.equals($scope.new_user.upassword, $scope.new_user.upassword2);
        };

        $scope.submitUser = function () {
            $scope.isPosting = true;
            $scope.new_user.udob = $filter('date')(new Date($scope.userDOB),'yyyy-MM-dd');
            $scope.new_user.upayment.cexpdate = $scope.paymentYear + '-' + $scope.paymentMonth;
            $scope.new_user.upayment.cnumber = $scope.userCard.cardNumber.toString();
            $scope.new_user.upayment.cvc = $scope.userCard.CVC.toString();
            $scope.new_user.upayment.ctype = getCardType($scope.new_user.upayment.cnumber);
            console.log(JSON.stringify($scope.new_user));
            userwsapi.postUser($scope.new_user).then(
                function () {
                    authenticationSvc.login($scope.new_user.uname, $scope.new_user.upassword).then(
                        function () {
                            $rootScope.$emit('Login');
                            $location.path('/account-info');
                        },
                        function () {
                            $rootScope.$emit('unLogin');
                            $location.path('/login.html');
                        }
                    );
                },
                function (err) {
                    if(err.data.errors){
                        $scope.errors = err.data.errors;
                    }
                    else if(err.data.Error){
                        $scope.errors = [err.data.Error];
                    }
                    else{
                        $scope.errors = ['Please fill all the required fields.'];
                    }
                }
            );
            $scope.isPosting = false;
        };

        $scope.sameAdd = function () {
            $scope.new_user.ubillingaddress = $scope.new_user.ushippingaddress;
        };

        getYears();


    }]);