app.controller('NavBarController', ['$scope', function($scope) {
    $scope.navbarOptions = [
        {
            platform: "PS4",
            imglogo: 'images/product-images/ps4-logo.jpg',
            consoles: [{id: 0, name:"Deals"}, {id:1, name: "PS4 Pro"},{id: 2, name: "PS4 Slim"}],
            accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
            topgames:["Deals","Action", "Fighting", "VR Games", "Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
        },
        {
            platform: "XBOX ONE",
            imglogo: 'images/product-images/xbox-one-logo.jpg',
            consoles: [{id: 0, name:"Deals"}, {id:1, name: "Xbox One S"},{id:2, name:"Xbox One"}],
            accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
            topgames:["Deals","Action", "Fighting", "Kinect Games", "Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
        },
        {
            platform: "3DS",
            imglogo: 'images/product-images/3ds-logo.jpg',
            consoles: [{id: 0, name:"Deals"}, {id:1, name: "Nintendo 3DS XL"},{id:2, name: "Nintendo 3DS"},{id:3, name: "Nitendo 2DS"}],
            accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
            topgames:["Deals","Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
        },
        {
            platform: "Wii U",
            imglogo: 'images/product-images/wii-u-logo.jpg',
            consoles: [{id: 0, name:"Deals"}, {id: 1, name: "Wii U"}],
            accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
            topgames:["Deals","Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
        }
    ];
}]);