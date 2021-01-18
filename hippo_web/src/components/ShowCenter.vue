<template>
  <div class="show_center">
    <h1>展示中心</h1>
    <a-button type="primary">
      展示中心
    </a-button>
    <a-locale-provider :locale="locale">
      <div>
        使用ant-design插件,尤其是时间选择插件
      </div>
    </a-locale-provider>

    <div ref="chart" style="height: 400px;width: 400px;">

    </div>
    <div ref="newchart" style="height: 400px;width: 400px;">

    </div>

  </div>
</template>

<script>
import zh_CN from 'ant-design-vue/lib/locale-provider/zh_CN';

export default {
  name: "ShowCenter",
  data() {
    return {
      locale: zh_CN,
    }
  },

  create() {
    this.$nextTick(() => {
      初始化图表
    })
  },
  mounted() {
    //图表1
    let myChart = this.$echarts.init(this.$refs.chart);
    myChart.setOption({
      title: {
        text: 'ECharts 入门示例1'
      },
      xAxis: {
        type: 'category',
        boundaryGap: false
      },
      yAxis: {
        type: 'value',
        boundaryGap: [0, '30%']
      },
      visualMap: {
        type: 'piecewise',
        show: false,
        dimension: 0,
        seriesIndex: 0,
        pieces: [{
          gt: 1,
          lt: 3,
          color: 'rgba(0, 180, 0, 0.5)'
        }, {
          gt: 5,
          lt: 7,
          color: 'rgba(0, 180, 0, 0.5)'
        }]
      },
      series: [
        {
          type: 'line',
          smooth: 0.6,
          symbol: 'none',
          lineStyle: {
            color: 'green',
            width: 5
          },
          markLine: {
            symbol: ['none', 'none'],
            label: {show: false},
            data: [
              {xAxis: 1},
              {xAxis: 3},
              {xAxis: 5},
              {xAxis: 7}
            ]
          },
          areaStyle: {},
          data: [
            ['2019-10-10', 200],
            ['2019-10-11', 400],
            ['2019-10-12', 650],
            ['2019-10-13', 500],
            ['2019-10-14', 250],
            ['2019-10-15', 300],
            ['2019-10-16', 450],
            ['2019-10-17', 300],
            ['2019-10-18', 100]
          ]
        }
      ]
    });

    //  图表2
    let newChart = this.$echarts.init(this.$refs.newchart);
    newChart.setOption({
      title: {
        text: 'ECharts 入门示例2'
      },
      tooltip: {},
      xAxis: {
        data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
      },
      yAxis: {},
      series: [{
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
      }]
    });
  }
}
</script>

<style scoped>

</style>
