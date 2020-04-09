<template>
    <div class="container">
        <div class="jumbotron mt-5">
            <div class="col-sm-8 mx-auto">
                <h1 class="text-center">PROFILE</h1>
            </div>
            <table class="table col-md-6 mx-auto">
                <tbody>
                  <tr>
                    <td></td>
                    <td><img src="../assets/images.png"></td>
                    <tr>
                    <tr>
                        <td>First Name</td>
                        <td>{{first_name}}</td>
                    </tr>
                    <tr>
                        <td>Last Name</td>
                        <td>{{last_name}}</td>
                    </tr>
                    <tr>
                        <td>Email</td>
                        <td>{{email}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button class="btn btn-lg btn-primary btn-block" @click="show" >Add To My Notes</button>
        <form id="hidden" v-on:submit.prevent="note" style="display:none;">
            <br><br><br>
                    <h1 class="h3 mb-3 font-weight-normal"><center>Enter The Notes</center></h1>
                    <div class="form-group">
                        <label for="details">Notes</label>
                        <input type="text" v-model="details" class="form-control" name="email" placeholder="Enter notes">
                    </div>
                    <button class="btn btn-lg btn-primary btn-block">Add</button>
                    <br><br><br>
                </form><br>
        <button class="btn btn-lg btn-primary btn-block" @click="view">View My Notes</button>
        <div id="hidden1" class="jumbotron mt-5" style="display:none;">
            <div class="col-sm-8 mx-auto">
                <h1 class="text-center">My Note</h1>
            </div>
            <table class="table col-md-6 mx-auto table table-dark" >
              <tr>
                <th>Date</th>
                <th>Notes</th>
              </tr>
                <tr v-for="notes in notes" :key="notes.details">
                 <td >
                      {{notes.date}}
                </td>
                <td>
                    {{notes.details}}
                </td>
                <td>
                  <img @click="delete1(notes.id,notes.date,notes.time)" src="../assets/minus.png" width="25px" height="25px">
                  </td>
              </tr>
            </table>
        </div>
    </div>
</template>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script>
import axios from 'axios'
import jwtDecode from 'jwt-decode'
import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-default.css'
import Vue from 'vue'
export default {
  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
      date: '',
      time: '',
      details: '',
      notes: []
    }
  },
  methods: {
    show () {
      var x = document.getElementById('hidden')
      var y = document.getElementById('hidden1')
      y.style.display = 'none'
      if (x.style.display === 'none') {
        x.style.display = 'block'
      } else {
        x.style.display = 'none'
      }
    },
    note () {
      axios.post('users/add', {
        email: this.email,
        details: this.details
      }).then(res => {
        this.details = ''
      })
    },
    view () {
      var x = document.getElementById('hidden1')
      var y = document.getElementById('hidden')
      y.style.display = 'none'
      if (x.style.display === 'none') {
        x.style.display = 'block'
      } else {
        x.style.display = 'none'
      }
      axios.post('users/getit', {
        email: this.email
      }).then(res => {
        this.notes = []
        var sData=res.data
        var details=sData['result']['details']
        var d=""
        var result=""
        var j=1
        for (var i=0;i<details.length;i++) {
          d=details[i].split("x")
          if (i==(details.length-1)) {
            this.notes.push({'index':j,'date':d[0],'time':d[1],'details':d[2]})
          } else {
            this.notes.push({'index':j,'date':d[0],'time':d[1],'details':d[2]})
          }
          j=j+1
        }
      })
    },
    delete1 (id,date,time) {
      //todo
      axios.post('users/delete', {
        email: this.email,
        date: date,
        time: time
      }).then(res => {
        this.$delete(this.notes,id)
        this.view()
        Vue.use(VueToast)
        this.$toast.open({
        message: "Note Deleted",
        type: "success",
        duration: 5000,
        dismissible: true
      })
        console.log(time,date)
      })
    }
  }
}
</script>
