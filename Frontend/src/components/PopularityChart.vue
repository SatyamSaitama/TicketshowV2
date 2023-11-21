<template>
    <div class="popularity-chart">
        <div class="chart-container-1">
            <canvas ref="showChartCanvas" width="100" height="100"></canvas>
            <button class="btn btn-success  " @click="downloadCSV('show_popularity')">Download CSV</button>
                
        </div>
        <div class="chart-container">
            <canvas ref="venueChartCanvas" width="100" height="100"></canvas>
            <button class="btn btn-success " @click="downloadCSV('venue_popularity')">Download CSV </button>
        </div>
  
    </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
    name: 'PopularityChart',
    props: {
        showPopularityData: {
            type: Array,
            required: true,
        },
        venuePopularityData: {
            type: Array,
            required: true,
        },
    },
    mounted() {
        this.renderChart();
        
    },
    methods: {
        downloadCSV(dataType) {
            
            if (dataType == 'show_popularity') {
                var csv = 'Title,Popularity\n';
                this.showPopularityData.forEach(function(row) {
                    csv += row.Title + ',' + row.Popularity + '\n';
                });
            } else {
                csv = 'Venue,Popularity\n';
                this.venuePopularityData.forEach(function(row) {
                    csv += row.Venue + ',' + row.Popularity + '\n';
                });
            }
            var hiddenElement = document.createElement('a');
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
            hiddenElement.target = '_blank';
            hiddenElement.download = dataType + '.csv';
            hiddenElement.click();

        },
        renderChart() {
           console.log("rendering chart");
        // Extracting show popularity and show titles from the provided data
            const showPopularity = this.showPopularityData.map(item => item.Popularity);
            const showTitles = this.showPopularityData.map(item => item.Title);
            console.log(showPopularity);
            // Extracting venue popularity and venue names from the provided data
            const venuePopularity = this.venuePopularityData.map(item => item.Popularity);
            const venueNames = this.venuePopularityData.map(item => item.Venue);

            // Creating the chart for shows
            new Chart(this.$refs.showChartCanvas, {
                type: 'bar',
                data: {
                    labels: showTitles,
                    datasets: [{
                        label: 'Show Popularity',
                        data: showPopularity,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });

            // Creating the chart for venues
            new Chart(this.$refs.venueChartCanvas, {
                type: 'pie',
                data: {
                    labels: venueNames,
                    datasets: [{
                        label: 'Venue Popularity',
                        data: venuePopularity,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)'
                            
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)'
                        ],
                        borderWidth: 1,
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        },
    },
};
</script>

<style scoped>
.popularity-chart {
    display: flex;
    justify-content: space-between;
}
.chart-container {
    flex: 1;
    margin: 10px;
    padding:10px;
    top : 10px;
    right : 10px;
    position : relative;
    
}
.chart-container-1 {
    flex: 1;
    margin: 10px;
    padding:10px;
    top : 10px;
    left : -50px;
    position : relative;
    
}

</style>
