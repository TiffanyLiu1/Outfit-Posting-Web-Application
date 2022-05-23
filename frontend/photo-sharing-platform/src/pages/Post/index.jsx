import React, { Component } from 'react'
import Layout from '@/components/Layout'
import Upload from '@/components/Upload'
import './index.css'

export default class Post extends Component {
	render() {
		return (
			<div>
				<Layout>
					<br />
					<br />
					<Upload />
				</Layout>
			</div>
		)
	}
}
