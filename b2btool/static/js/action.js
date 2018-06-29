/*
File: action.js
Description: Customized actions for B2B tool
Date: 29/06/2018
Author: Saurabh Badhwar
*/

var $selectedPrimaryBuildTag, $selectedSecondaryBuildTag;
var $selectedPrimaryHostName, $selectedSecondaryHostName;
var $selectedBenchmark;
var $selectedMetric;
var $primaryChart, $secondaryChart;

function getBuildtags() {
    $.getJSON('/tags', function(data){
        $.each(data['tags'], function(key, val){
            $option_val = "<option value='" + val + "'>" + val + "</option>"
            $("#build-tag, #build-tag-1").append($option_val);
        });
    })

}

function getHostname(build_tag, target) {
    var $queryURL = "/hosts?build_tag=" + build_tag
    $(target).html("");
    $.getJSON($queryURL, function(data){
        $.each(data['hosts'], function(key, val){
            $option_val = "<option value='" + val + "'>" + val + "</option>"
            $(target).append($option_val);
        })
    })
}

function getBenchmarks(buildTag, hostname, target) {
    var $queryURL = "/benchmarks?build_tag=" + buildTag + "&hostname=" + hostname
    $(target).html("");
    $.getJSON($queryURL, function(data){
        console.log(data);
        $.each(data['benchmarks'], function(key, val){
            $option_val = "<option value='" + val + "'>" + val + "</option>"
            $(target).append($option_val);
        })
    })
}

function getBuildMetrics(buildTag, benchmark, hostname, target) {
    var $queryURL = "/build_metrics?build_tag=" + buildTag + "&hostname=" + hostname + "&benchmark=" + benchmark
    $(target).html("");
    $.getJSON($queryURL, function(data){
        console.log(data);
        $.each(data['metrics'], function(key, val){
            $option_val = "<option value='" + val + "'>" + val + "</option>"
            $(target).append($option_val);
        })
    })
}

function getMetrics(metric, target) {
    var $queryURL = "/leaf_metrics?query_path=" + metric
    $(target).html("");
    $.getJSON($queryURL, function(data){
        console.log(data);
        $.each(data['metric_paths'], function(key, val){
            $option_val = "<option value='" + val + "'>" + val + "</option>"
            $(target).append($option_val);
        })
    })
}

function getMetricData(buildTag, benchmark, hostname, metric, target) {
    var $queryURL = "/build_metrics?build_tag=" + buildTag + "&hostname=" + hostname + "&benchmark=" + benchmark + "&query_path=" + metric
    $(target).html("");
    $.getJSON($queryURL, function(data){
        console.log(data);
        xData = ['x']
        yData = [metric]
        $.each(data['dataset'], function(key, val){
            yData.push(val[0]);
            //d = new Date(val[1])
            //xData.push(d.toISOString())
            xData.push(val[1])
        })
        $primaryChart = setupChart(target, xData, yData);
    })    
}

function setupChart(target, xData, yData) {
    var chart = c3.generate({
        bindto: target,
        data: {
            x: 'x',
            columns: [
                xData,
                yData
            ]
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%H:%M:%S',
                    count: 10
                }
            }
        },
        subchart: {
            show: true
        }
    })
    return chart
}

$(document).ready(function(){
    getBuildtags();
    $("#build-tag").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        $selectedPrimaryBuildTag = $selectedValue;
        getHostname($selectedValue, $("#hostname"))
    });
    $("#build-tag-1").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        $selectedSecondaryBuildTag = $selectedValue;
        getHostname($selectedValue, $("#hostname-1"))
    });
    $("#hostname").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        $selectedPrimaryHostName = $selectedValue;
        getBenchmarks($selectedPrimaryBuildTag, $selectedValue, $("#benchmark"))
    });
    $("#hostname-1").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        $selectedSecondaryHostName = $selectedValue;
        getBuildMetrics($selectedSecondaryBuildTag, $selectedBenchmark, $selectedValue, $("#metric-class-1"));
    });
    $("#benchmark").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        $selectedBenchmark = $selectedValue;
        getBuildMetrics($selectedPrimaryBuildTag, $selectedValue, $selectedPrimaryHostName, $("#metric-class"));
    })
    $("#metric-class").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        getMetrics($selectedValue, $("#metric"))
    })
    $("#metric-class-1").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        getMetrics($selectedValue, $("#metric-1"))
    })
    $("#metric").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        getMetricData($selectedPrimaryBuildTag,$selectedBenchmark,$selectedPrimaryHostName, $selectedValue, '#compare-block-1-chart');
    })
    $("#metric-1").on('change click', function(e){
        var $selectedValue;
        $.each(this.selectedOptions, function(key, value){
            $selectedValue = value.value;
        })
        getMetricData($selectedSecondaryBuildTag,$selectedBenchmark,$selectedSecondaryHostName, $selectedValue, '#compare-block-2-chart');
    })
})