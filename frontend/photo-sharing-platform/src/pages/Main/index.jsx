import React, { Component } from 'react'
import Layout from '@/components/Layout'
import URLS from '@/request/url'
import axios from 'axios'
import { withRouter } from '@/router/withRouter'
import ImgPage from '@/components/ImgPage'
import ToPost from '@/components/ToPost'
import Loading from '@/components/Loading'
import './index.css'

class Main extends Component {

	state = {
		resultImage: [],
		isFirst: true,
		isLoading: false
	}

	async componentDidMount() {
		this.setState({ isLoading: true });
		const input = window.location.pathname.split('/').pop();
		const requestParams = {
			input,
			account: JSON.parse(localStorage.getItem('Account')).account
		}
		let res = await axios.post(URLS.USER_SEARCH_PHOTO, requestParams);
		let { body } = res.data;
		let result = body || [];
		this.setState({ resultImage: result, isLoading: false });
	}

	setResultImage = (curImgId) => {
		const copyResultImage = [...this.state.resultImage];
		this.setState({
			resultImage: copyResultImage.map(item => item.imgId === curImgId ? { ...item, liked: !item.liked } : item)
		});
	}

	render() {
		const { resultImage, isLoading } = this.state;
		return (
			<div>
				<Layout>
					{
						isLoading ?
							<Loading />
							:
							<ImgPage
								data={resultImage}
								setResultImage={this.setResultImage}
							/>
					}
				</Layout>
				<ToPost />
			</div>
		)
	}
}

export default withRouter(Main)