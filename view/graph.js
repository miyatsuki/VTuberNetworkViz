Vue.config.devtools = true;

onload = function() {

    const app = new Vue({
        el: '#app',
        data: {
          items: plot_data,
          collab_times_mat: collab_times_mat,
          debut_map: debut_map,
          pca_vec_all: [],
          song_list: [],
          singer_list: ['YuNi'],
          user_song_list: [],
          selected_video_id: ""
        },
        methods: {
          getClipDefName: function(pos_info)
          {
            return "clipPath_" + pos_info.id
          },
          getClipUsageName: function(pos_info){
            return "clip-path: url(#clipPath_" + pos_info.id + ");"
          },
          getLineWidth: function(from_index, to_index){
            sum = 0
            collab_array = collab_times_mat[from_index]
            for(var i = 0; i < collab_array.length; i++){
              sum += collab_array[i]
            }
            return collab_times_mat[from_index][to_index]/sum
          },
          getDebutTypeColor: function(pos_info){
            debut_type = debut_map[pos_info.name]
            console.log(debut_type)
            if(typeof debut_type === "undefined"){
              return "black"
            }

            /* typeA */
            /*
            if(debut_type.indexOf("にじさんじ") == 0){
              return "red"
            }else if(debut_type.indexOf("ゲーマーズ") == 0){
              return "blue"
            }else if(debut_type.indexOf("SEEDs") == 0){
              return "green"
            }else if(debut_type.indexOf("統合後") == 0){
              return "yellow"
            }*/

            /* typeB */
            //にじさんじ1期
            //にじさんじ2期
            //ゲーマーズ1期
            //SEEDs1期
            //ゲーマーズ2期
            //ゲーマーズ3期
            //SEEDs2期1弾
            //SEEDs2期2弾
            //SEEDs2期3弾
            //統合後20190108
            //統合後20190117
            //統合後20190128
            //統合後20190308
            //統合後20190322
            //統合後20190402
            //統合後20190429

            if(debut_type.indexOf("にじさんじ1期") == 0){
              return "red"
            }else if(debut_type.indexOf("にじさんじ2期") == 0){
              return "pink"
            }else if(debut_type.indexOf("ゲーマーズ1期") == 0){
              return "navy"
            }else if(debut_type.indexOf("ゲーマーズ2期") == 0){
              return "blue"
            }else if(debut_type.indexOf("ゲーマーズ3期") == 0){
              return "skyblue"
            }else if(debut_type.indexOf("SEEDs1期") == 0){
              return "darkgreen"
            }else if(debut_type.indexOf("SEEDs2期1弾") == 0){
              return "green"
            }else if(debut_type.indexOf("SEEDs2期2弾") == 0){
              return "lime"
            }else if(debut_type.indexOf("SEEDs2期3弾") == 0){
              return "palegreen"
            }else if(debut_type.indexOf("統合後20190108") == 0){
              return "saddlebrown"
            }else if(debut_type.indexOf("統合後20190117") == 0){
              return "peru"
            }else if(debut_type.indexOf("統合後20190128") == 0){
              return "yellow"
            }else if(debut_type.indexOf("統合後20190308") == 0){
              return "black"
            }else if(debut_type.indexOf("統合後20190322") == 0){
              return "gray"
            }else if(debut_type.indexOf("統合後20190402") == 0){
              return "white"
            }
          },
          getNearestSingersFromSong: function(){

            console.log("getNearestSingersFromSong")
            if(this.user_song_list.length == 0){
              return []
            }

            distance_list = []
            for(var i = 0; i < plot_data.length; i++){
              common_song_count = 0
              for(var j = 0; j < this.user_song_list.length; j++){
                song = this.user_song_list[j]
                if(plot_data[i]["song"].indexOf(song) > -1){
                  common_song_count++
                }
              }

              simirarity = -1
              if(common_song_count > 0){
                simirarity = common_song_count/(Math.sqrt(this.user_song_list.length)*Math.sqrt(plot_data[i]["song"].length))
              }

              distance_list.push(1 - simirarity)
            }

            for(var to = 0; to < distance_list.length; to++){
              for(var i = 0; i < dist_mat.length; i++){
                distance = distance_list[i] + dist_mat[i][to]
                if(distance_list[to] > distance){
                  distance_list[to] = distance
                }
              }
            }

            max_distance = 0;
            for(var i = 0; i < distance_list.length; i++){
              if(max_distance < distance_list[i]){
                max_distance = distance_list[i]
              }
            }

            singer_id_list = []
            for(var i = 0; i < plot_data.length; i++){
              if(this.singer_list.indexOf(plot_data[i].name) > -1){
                singer_id_list.push(plot_data[i].singer_id)
              }
            }

            sort_index = []
            for(var i = 0; i < distance_list.length; i++){
              is_inserted = false
              for(var j = 0; j < i; j++){
                if(distance_list[sort_index[j]] > distance_list[i]){
                  is_inserted = true
                  sort_index.splice(j, 0, i)
                  break
                }
              }

              if(!is_inserted){
                sort_index.push(i)
              }
            }

            result = []
            for(var i = 0; i < 20; i++){
              singer_id = sort_index[i]
              result.push({name: plot_data[singer_id].name, simirarity: (max_distance-distance_list[singer_id])/max_distance})
            }

            for(var i = sort_index.length-6; i < sort_index.length; i++){
              singer_id = sort_index[i]
              result.push({name: plot_data[singer_id].name, simirarity: (max_distance-distance_list[singer_id])/max_distance})
            }

            console.log(result)
            return result
          },
          dist2vec(singer_list){
            // singer_listが0だったら全員分やる
            console.log(singer_list)
            var singer_list_tmp = []
            if(singer_list.length == 0){
              for(var i = 0; i < plot_data.length; i++){
                  singer_list_tmp.push(plot_data[i].name)
              }
            }

            // singer_listが1だったら選曲傾向とかないので0, 0で戻す
            if(singer_list.length == 1){
              return [{singer: singer_list[0], posX: 0, posY: 0}]
            }

            // singer_listが2だったら正規化したあとの距離1なの確定なので1, 1と-1, -1で戻す
            if(singer_list.length == 2){
              return [{singer: singer_list[0], posX: 0.9, posY: 0.9}, {singer: singer_list[1], posX: -0.9, posY: -0.9}]
            }

            // それ以上だったらちゃんと計算する
            for(var i = 0; i < singer_list.length; i++){
              singer_list_tmp.push(singer_list[i])
            }

            singer_id_list = []
            for(var i = 0; i < plot_data.length; i++){
              if(singer_list_tmp.indexOf(plot_data[i].name) > -1){
                singer_id_list.push(plot_data[i].singer_id)
              }
            }

            var dist_mat_calc = []
            for(var i = 0; i < singer_id_list.length; i++){
              dist_mat_row = []
              for(var j = 0; j < singer_id_list.length; j++){
                dist_mat_row.push(dist_mat[singer_id_list[i]][singer_id_list[j]])
              }
              dist_mat_calc.push(dist_mat_row)
            }

            console.log(dist_mat_calc)
            vectors = PCA.getEigenVectors(dist_mat_calc)

            pos_list = new Array(vectors[0]["vector"].length)
            xSum = 0
            ySum = 0
            for(var i = 0; i < vectors[0]["vector"].length; i++){
              pos_list[i] = [-vectors[0]["vector"][i], vectors[1]["vector"][i]]
              xSum += pos_list[i][0]
              ySum += pos_list[i][1]
            }
            xAve = xSum/pos_list.length
            yAve = ySum/pos_list.length
        
            xMax = 0
            yMax = 0
            for(var i = 0; i < vectors[0]["vector"].length; i++){
              pos_list[i][0] -= xAve
              pos_list[i][1] -= yAve
        
              if (xMax < Math.abs(pos_list[i][0])){
                xMax = Math.abs(pos_list[i][0])
              }
        
              if (yMax < Math.abs(pos_list[i][1])){
                yMax = Math.abs(pos_list[i][1])
              }
            }
        
            xScale = 0.9/xMax
            yScale = 0.9/yMax
        
            for(var i = 0; i < pos_list.length; i++){
              pos_list[i][0] *= xScale
              pos_list[i][1] *= yScale
            }
            
            result = []
            console.log(pos_list)
            for(var i = 0; i < singer_list_tmp.length; i++){
              result.push({singer: singer_list_tmp[i], posX: pos_list[i][0], posY: pos_list[i][1]})
            }

            return result
          }
        }
    })

    var elems = document.querySelectorAll('.chips')
    var all_singer_list = []
    for(var i = 0; i < plot_data.length; i++){
      all_singer_list.push(plot_data[i]["name"])
    }

    singer_autocomplete = {}
    for(var i = 0; i < all_singer_list.length; i++){
      singer_autocomplete[all_singer_list[i]] = null
    }

    var instances = M.Chips.init(elems, {
      data : [
        {tag: 'YuNi'}
      ],
      placeholder: 'Vsinger',
      secondaryPlaceholder: '+Vsinger',
      autocompleteOptions: {
        data: singer_autocomplete,
        limit: Infinity,
        minLength: 1
      },
      onChipAdd: function(){
        app.singer_list.push(this.chipsData[this.chipsData.length - 1]["tag"])
      },
      onChipDelete: function(){
        existing_tags = []
        for(var i = 0; i < this.chipsData.length; i++){
          existing_tags.push(this.chipsData[i]["tag"])
        }

        for(var i = app.singer_list.length; i >= 0; i--){
          if(existing_tags.indexOf(app.singer_list[i]) == -1){
            app.singer_list.splice(i, 1)
          }
        }
      }
    })

    var elems = document.querySelectorAll('.chips_songs')
};