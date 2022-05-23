import React, { Component } from 'react'
// Import centrally managed url paths
import URLS from '@/request/url'
import axios from 'axios'
import { withRouter } from '@/router/withRouter'
import { v4 as uuid } from 'uuid'
import './index.css'

class Upload extends Component {
    state = {
        previewImgSrc: '',
        title: '',
        postContent: '',
        label1: '',
        label2: ''
    }

    // change upload button
    upload = () => {
        const uploadBtn = document.getElementById('uploadFileInput');
        uploadBtn.click();
    }

    // get url of uploaded image
    getObjectURL = (file) => {
        let url = null;
        if (window.createObjectURL !== undefined) { // basic
            url = window.createObjectURL(file);
        } else if (window.URL !== undefined) { // mozila(firefox)
            url = window.URL.createObjectURL(file);
        } else if (window.webkitURL !== undefined) { // webkit or chrome
            url = window.webkitURL.createObjectURL(file);
        }
        return url;
    }

    // set preview image
    changeValue = (e) => {
        let file = e.target.files[0];
        let url = URL.createObjectURL(file);
        this.setState({ previewImgSrc: url });
    }

    setTitle = (val) => {
        this.setState({ title: val });
    }

    setLabel1 = (e) => {
        this.setState({ label1: e.target.value });
    }

    setLabel2 = (e) => {
        this.setState({ label2: e.target.value });
    }

    setPostContent = (val) => {
        this.setState({ postContent: val });
    }

    handleSubmit = async (e) => {
        e.preventDefault();
        // get form file
        const files = document.getElementById('uploadFileInput').files[0];
        // set labels combination
        const { label1, label2 } = this.state;
        const label = label2.length ? label1 + ',' + label2 : label1;
        // set request body
        const config = {
            headers: {
                'Content-Type': files.type,
                'x-amz-meta-customLabels': label,
                'x-amz-meta-account': JSON.parse(localStorage.getItem('Account')).account,
                'x-amz-meta-postContent': this.state.postContent,
                'x-amz-meta-title': this.state.title
            }
        }

        let url = URLS.USER_POST_MESSAGE + '/post-s3-bucket/' + uuid() + '-' + files.name;
        await axios.put(url, files, config);
        alert('Successfully posted! Now navigate to the detail you just posted!');
        
        this.props.navigate('/userInfo');
    }

    render() {
        const { previewImgSrc } = this.state;
        return (
            <div className='container'>
                <form onSubmit={this.handleSubmit} className="row">
                    <div className="col-md-7 uploadLeft">
                        <div className='uploadLeftBox'>
                            <div className='uploadLeftBoxInner' onClick={this.upload}>
                                <div className="uploadIconBox">
                                    <i className="fas fa-regular fa-plus"></i>
                                    <br />
                                    <p>Click to upload</p>
                                </div>
                                <input
                                    type="file"
                                    id="uploadFileInput"
                                    name="file"
                                    onChange={this.changeValue}
                                />
                            </div>
                        </div>
                    </div>
                    <div className="col-md-5">
                        <div className="col-md-12">
                            <div className="previewImageBox">
                                <img src={previewImgSrc} alt="img" />
                            </div>
                        </div>
                        <div className="col-md-12 input-group-lg">
                            <br />
                            <input
                                type="text"
                                className="form-control"
                                id="title"
                                placeholder='Add your title'
                                onChange={e => this.setTitle(e.target.value)}
                            />
                        </div>
                        <div className="col-md-12 input-group-lg">
                            <br />
                            <div className='row'>
                                <div className='col-md-6'>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="title"
                                        placeholder='Attach your label1'
                                        value={this.state.label1}
                                        onChange={this.setLabel1}
                                    />
                                </div>
                                <div className='col-md-6'>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="title"
                                        placeholder='Attach your label2'
                                        value={this.state.label2}
                                        onChange={this.setLabel2}
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="col-md-12">
                            <br />
                            <textarea
                                type="text"
                                className="form-control"
                                rows="5"
                                placeholder="Write your post..."
                                onChange={e => this.setPostContent(e.target.value)}
                            />
                        </div>
                        <div className="col-md-12">
                            <br />
                            <button type="submit" className="postBtn btn btn-danger">Post</button>
                        </div>
                    </div>
                </form>
            </div>
        )
    }
}

export default withRouter(Upload)