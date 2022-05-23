import React, { Component } from 'react'
import { Link } from "react-router-dom";
import './index.css'

export default class ToPost extends Component {
    render() {
        return (
            <div>
                <Link to='/post' className='add'>
                    <i className="fas fa-plus"></i>
                </Link>
            </div>
        )
    }
}
