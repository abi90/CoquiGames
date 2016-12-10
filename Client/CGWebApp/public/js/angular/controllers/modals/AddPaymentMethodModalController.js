/**
 * Created by abi on 12/10/16.
 */
app.controller('AddPaymentMethodModalController',
    [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', '$location',
        function ($scope, authenticationSvc, $rootScope, Popeye, $location){

            $scope.selectedPayment = {ppreferred: false};
            $scope.userCard = {cardNumber: null, CVC: null};
            $scope.paymentYear = '';
            $scope.paymentMonth = '';
            $scope.yearOptions=[];

            $scope.patterns = {
                ccard: /^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13})$/g,
                bigText: '[a-zA-Z\\d\\.\\:\\,\\;\\s\\-]+',
                cvc: '\\d{3}'
            };

            var getUser = function(){
                var userInfo = authenticationSvc.getUserInfo();
                if(!userInfo){
                    $rootScope.$emit('unLogin');
                    $location.path('/login.html');
                    return Popeye.closeCurrentModal(null);
                }
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
                if(cardNumber.match($scope.patterns.ccard)){
                    result = (cardNumber.match(visa)) ? (cardNumber.match(visa).length == 1) ? 'Visa':result:result;
                    result = (cardNumber.match(aExp)) ? (cardNumber.match(aExp).length == 1) ? 'American Express':result:result;
                    result = (cardNumber.match(mCard)) ? (cardNumber.match(mCard).length == 1) ? 'Master Card':result:result;
                }
                return result;
            };



            $scope.submit = function() {
                $scope.selectedPayment.cexpdate = $scope.paymentYear + '-' + $scope.paymentMonth;
                $scope.selectedPayment.cnumber = $scope.userCard.cardNumber.toString();
                $scope.selectedPayment.cvc = $scope.userCard.CVC.toString();
                $scope.selectedPayment.ctype = getCardType($scope.selectedPayment.cnumber);
                return Popeye.closeCurrentModal($scope.selectedPayment);
            };

            $scope.cancel = function () {
                return Popeye.closeCurrentModal(null);
            };

            getYears();
            getUser();

        }]);