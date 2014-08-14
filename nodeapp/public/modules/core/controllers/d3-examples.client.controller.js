'use strict';

angular.module('core').controller('D3GitController', ['$scope', '$http',
	function($scope, $http) {
  		// initialize the model
    $scope.user = 'digirithm';
    $scope.repo = 'tweetsense';

    // helper for formatting date
    var humanReadableDate = function (d) {
      return d.getUTCMonth()+1 + '/' + d.getUTCDate();
    };

    // helper for reformatting the Github API response into a form we can pass to D3
    var reformatGithubResponse = function (data) {
      // sort the data by author date (rather than commit date)
      data.sort(function (a, b) {
        if (new Date(a.commit.author.date) > new Date(b.commit.author.date)) {
          return -1;
        } else {
          return 1;
        }
      });

      // date objects representing the first/last commit dates
      var date0 = new Date(data[data.length - 1].commit.author.date);
      var dateN = new Date(data[0].commit.author.date);

      // the number of days between the first and last commit
      var days = Math.floor((dateN - date0) / 86400000) + 1;

      // map authors and indexes
      var uniqueAuthors = []; // map index -> author
      var authorMap = {}; // map author -> index
      data.forEach(function (datum) {
        var name = datum.commit.author.name;
        if (uniqueAuthors.indexOf(name) === -1) {
          authorMap[name] = uniqueAuthors.length;
          uniqueAuthors.push(name);
        }
      });

      // build up the data to be passed to our d3 visualization
      var formattedData = [];
      formattedData.length = uniqueAuthors.length;
      var i, j;
      for (i = 0; i < formattedData.length; i++) {
        formattedData[i] = [];
        formattedData[i].length = days;
        for (j = 0; j < formattedData[i].length; j++) {
          formattedData[i][j] = {
            x: j,
            y: 0
          };
        }
      }
      data.forEach(function (datum) {
        var date = new Date(datum.commit.author.date);
        var curDay = Math.floor((date - date0) / 86400000);
        formattedData[authorMap[datum.commit.author.name]][curDay].y += 1;
        formattedData[0][curDay].date = humanReadableDate(date);
      });

      // add author names to data for the chart's key
      for (i = 0; i < uniqueAuthors.length; i++) {
        formattedData[i][0].user = uniqueAuthors[i];
      }

      return formattedData;
    };

    $scope.getCommitData = function () {
      $http({
        method: 'GET',
        url:'https://api.github.com/repos/' +
          $scope.user +
          '/' +
          $scope.repo +
          '/commits'
      }).
      success(function (data) {
        // attach this data to the scope
        $scope.data = reformatGithubResponse(data);

        // clear the error messages
        $scope.error = '';
      }).
      error(function (data, status) {
        if (status === 404) {
          $scope.error = 'That repository does not exist';
        } else {
          $scope.error = 'Error: ' + status;
        }
      });
  	}
  }

]);

angular.module('core').controller('D3ChoroplethController', ['$scope', '$http',
  function($scope, $http) {
  // chorpleth

    var width = 960,
        height = 600;
     
    var rateById = d3.map();
     
    var quantize = d3.scale.quantize()
        .domain([0, .15])
        .range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));
     
    var projection = d3.geo.albersUsa()
        .scale(1280)
        .translate([width / 2, height / 2]);
     
    var path = d3.geo.path()
        .projection(projection);
     
    var svg = d3.select("#choropleth_demo").append("svg")
        .attr("width", width)
        .attr("height", height);
     
    queue()
        .defer(d3.json, "/testdata/us.json")
        .defer(d3.tsv, "/testdata/unemployment.tsv", function(d) { rateById.set(d.id, +d.rate); })
        .await(ready);
     
    function ready(error, us) {
      svg.append("g")
          .attr("class", "counties")
        .selectAll("path")
          .data(topojson.feature(us, us.objects.counties).features)
        .enter().append("path")
          .attr("class", function(d) { return quantize(rateById.get(d.id)); })
          .attr("d", path);
     
      svg.append("path")
          .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
          .attr("class", "states")
          .attr("d", path);
    }
     
    d3.select(self.frameElement).style("height", height + "px");
  }
]);
