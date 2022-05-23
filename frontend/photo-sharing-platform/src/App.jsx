import React, { Component } from 'react'
import AppRouter from '@/router'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'

export default class App extends Component {
  render() {
    return (
      <div>
        <AppRouter/>
      </div>
    )
  }
}

