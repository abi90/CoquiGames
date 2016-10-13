var app = angular.module('MainApp', ['ngRoute','ui.bootstrap.demo','ngAnimate', 'ngSanitize']);

app.config(['$httpProvider', '$routeProvider', function ($httpProvider, $routeProvider) {
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = false;
    delete $httpProvider.defaults.headers.common["X-Requested-With"];
    $httpProvider.defaults.headers.common["Accept"] = "application/json";
    $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
  $routeProvider
    .when('/', {
      controller: 'HomeController',
      templateUrl: 'views/home.html'
    })
      .when('/404.html', {
          controller: 'HomeController',
          templateUrl: 'views/404.html'
      })
      .when('/index.html', {
          controller: 'HomeController',
          templateUrl: 'views/home.html'
      })
      .when('/about.html', {
          controller: 'HomeController',
          templateUrl: 'views/about.html'
      })
      .when('/cart.html', {
          controller: 'HomeController',
          templateUrl: 'views/cart.html',
          resolve: {
              auth: function ($q, authenticationSvc) {
                  var userInfo = authenticationSvc.getUserInfo();
                  if (userInfo) {
                      return $q.when(userInfo);
                  } else {
                      return $q.reject({ authenticated: false });
                  }
              }
          }
      })
      .when('/category-grid.html', {
          controller: 'HomeController',
          templateUrl: 'views/category-grid.html'
      })
      .when('/category-list.html', {
          controller: 'HomeController',
          templateUrl: 'views/category-list.html'
      })
      .when('/compare.html', {
          controller: 'HomeController',
          templateUrl: 'views/compare.html'
      })
      .when('/contact.html', {
          controller: 'HomeController',
          templateUrl: 'views/contact.html'
      })
      .when('/login.html', {
          controller: 'LoginController',
          templateUrl: 'views/login.html'
      })
      .when('/product.html', {
          controller: 'HomeController',
          templateUrl: 'views/product.html'
      })
      .when('/product-full.html', {
          controller: 'HomeController',
          templateUrl: 'views/product-full.html'
      })
      .when('/register.html', {
          controller: 'HomeController',
          templateUrl: 'views/register.html'
      })
      .when('/typography.html', {
          controller: 'HomeController',
          templateUrl: 'views/typography.html'
      })
      .when('/wishlist', {
          controller: 'AccountController',
          templateUrl: 'views/wishlist.html',
          resolve: {
              auth: function ($q, authenticationSvc) {
                  var userInfo = authenticationSvc.getUserInfo();
                  if (userInfo) {
                      return $q.when(userInfo);
                  } else {
                      return $q.reject({ authenticated: false });
                  }
              }
          }
      })
      .when('/search-list', {
          controller: 'HomeController',
          templateUrl: 'views/search-list.html'
      })
      .when('/search-grid', {
          controller: 'HomeController',
          templateUrl: 'views/search-list.html'
      })
      .when('/account-info', {
          controller: 'AccountController',
          templateUrl: 'views/account-info.html',
          resolve: {
              auth: function ($q, authenticationSvc) {
                  var userInfo = authenticationSvc.getUserInfo();
                  if (userInfo) {
                      return $q.when(userInfo);
                  } else {
                      return $q.reject({ authenticated: false });
                  }
              }
          }
      })
      .when('/account-orders', {
          controller: 'AccountController',
          templateUrl: 'views/account-orders.html',
          resolve: {
              auth: function ($q, authenticationSvc) {
                  var userInfo = authenticationSvc.getUserInfo();
                  if (userInfo) {
                      return $q.when(userInfo);
                  } else {
                      return $q.reject({ authenticated: false });
                  }
              }
          }
      })
      .when('/account-payment', {
          controller: 'AccountController',
          templateUrl: 'views/account-payment.html',
          resolve: {
              auth: function ($q, authenticationSvc) {
                  var userInfo = authenticationSvc.getUserInfo();
                  if (userInfo) {
                      return $q.when(userInfo);
                  } else {
                      return $q.reject({ authenticated: false });
                  }
              }
          }
      })
      .when('/checkout', {
          controller: 'AccountController',
          templateUrl: 'views/checkout.html',
          resolve: {
              auth: function ($q, authenticationSvc) {
                  var userInfo = authenticationSvc.getUserInfo();
                  if (userInfo) {
                      return $q.when(userInfo);
                  } else {
                      return $q.reject({ authenticated: false });
                  }
              }
          }
      })
      .when('/account-address', {
          controller: 'AccountController',
          templateUrl: 'views/account-address.html',
          resolve: {
              auth: function ($q, authenticationSvc) {
                  var userInfo = authenticationSvc.getUserInfo();
                  if (userInfo) {
                      return $q.when(userInfo);
                  } else {
                      return $q.reject({ authenticated: false });
                  }
              }
          }
      })
      .otherwise({
          redirectTo: '/'
      });

}]);

app.run(["$rootScope", "$location", function ($rootScope, $location) {

    $rootScope.$on("$routeChangeSuccess", function (userInfo) {
        console.log(userInfo);
    });

    $rootScope.$on("$routeChangeError", function (event, current, previous, eventObj) {
        if (eventObj.authenticated === false) {
            $location.path("/login");
        }
    });
}]);
