// Put your application scripts here
Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

const renderChart = async (url) => {
    const res = await fetch(url);
    return await res.json();
};

renderChart('/api/v1/month')
    .then(jsonData => {

        let chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
                defaultSeriesType: 'area',
            },

            title: {
                text: '食べたリンゴたち (月別)'
            },

            xAxis: {
                categories: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            },

            yAxis: {
                title: {
                    text: '個'
                },

                plotLines: [{
                    value: 0,
                    width: 1
                }]
            },

            tooltip: {
                shared: false,
                formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                        this.x + ': ' + this.y + ' 個';
                }
            },

            plotOptions: {
                area: {
                    stacking: 'normal'
                }
            },

            series: jsonData
        });
    });