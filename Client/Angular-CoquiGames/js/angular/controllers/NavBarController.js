app.controller('NavBarController', ['$scope', function($scope) {
    $scope.navbarOptions = [
        {
            platform: "PS4",
            imglogo: 'images/product-images/ps4-logo.jpg',
            consoles: [{id: 0, name:"PS4 Slim"}, {id:1, name: "PS4 Old"}],
            accesories: ["controller", "headphones"],
            topgames:["NBA 2k17", "BattleField 4"]
        },
        {
            platform: "XBOX ONE",
            imglogo: 'images/product-images/xbox-one-logo.jpg',
            consoles: [{id: 0, name:"PS4 Slim"}, {id:1, name: "PS4 Old"}],
            accesories: ["controller", "headphones"],
            topgames:["NBA 2k17", "BattleField 4"]
        },
        {
            platform: "3DS",
            imglogo: 'images/product-images/3ds-logo.jpg',
            consoles: [{id: 0, name:"PS4 Slim"}, {id:1, name: "PS4 Old"}],
            accesories: ["controller", "headphones"],
            topgames:["NBA 2k17", "BattleField 4"]
        },
        {
            platform: "Wii U",
            imglogo: 'images/product-images/wii-u-logo.jpg',
            consoles: [{id: 0, name:"PS4 Slim"}, {id: 1, name: "PS4 Old"}],
            accesories: ["controller", "headphones"],
            topgames:["NBA 2k17", "Battle Fiel 4"]
        }
    ];
}]);