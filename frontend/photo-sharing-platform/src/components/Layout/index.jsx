import React, { Component } from 'react'
import Header from '@/components/Header'
import './index.css'

export default class Layout extends Component {
  render() {
    return (
      <div>
        <Header />
        <br></br>
        <main>{ this.props.children }</main>
      </div>
    )
  }
}
