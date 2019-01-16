// vendor
import React, { Component } from 'react';
import DocumentTitle from 'react-document-title';

// proj
import { Layout } from '../../layouts';
import { BoardContainer } from '../../containers';

export default class BoardPage extends Component {
    render() {
        return (
            <DocumentTitle title='EPAM Bot Challenge :: Login'>
                <Layout>
                    <BoardContainer />
                </Layout>
            </DocumentTitle>
        );
    }
}
