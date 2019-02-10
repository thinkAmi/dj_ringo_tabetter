const renderChart = async (url) => {
    const res = await fetch(url);
    return await res.json();
};

renderChart('/api/v1/total')
    .then(jsonData => {
        const chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
                defaultSeriesType: 'pie',
            },

            title: {
                text: '食べたリンゴたち'
            },

            tooltip: {
                formatter: function () {
                    // (注) アロー関数にすると表示されなくなる
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
                data: jsonData
            }]
        });
    });

