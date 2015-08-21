$(function () {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            defaultSeriesType: 'pie',
        },

        title: {
            text: '食べたリンゴたち'
        },

        tooltip: {
            formatter: function () {
                return '<b>' + this.point.name + '</b>: ' + this.point.y + '個';
            }
        },

        plotOptions: {
            pie: {
                allowPointSelect: true,
                showInLegend: true
            }
        },


        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: 0,
            y: 100
        },

        series: [{
            data: [
            ]
        }]
    });

    $.getJSON('/api/v1/total', function(res){
        //$.getJSON('https://ringo-tabetter-api.herokuapp.com/api/v1/total?callback=?', function (res) {
        $.each(res, function (i, json) {
            chart.series[0].addPoint({
                name: json['name'],
                y: json['quantity'],
                color: json['color']
            });
        });
    });
});