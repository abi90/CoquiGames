var app = angular.module('MainApp', ['ngRoute','ui.bootstrap.demo']);

app.config(function ($routeProvider) {
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
          templateUrl: 'views/cart.html'
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
          controller: 'HomeController',
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
          controller: 'HomeController',
          templateUrl: 'views/wishlist.html'
      })
      .otherwise({
      redirectTo: '/'
      });

});
