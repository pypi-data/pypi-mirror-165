import * as React from "react";
import Layout from "../components/layout";
import { graphql } from "gatsby";
import { MessageBox } from "../components/atoms";
import GenerateView from "../components/views/generate";

// markup
const IndexPage = ({ data }: any) => {
  return (
    <Layout meta={data.site.siteMetadata} title="Home" link={"/"}>
      <main className="">
        <div className="mb-6">
          <MessageBox title={`Welcome to ${data.site.siteMetadata.title}`}>
            <div>
              Peacasso is a UI tool to help you generate art with AI models
              (diffusion) models.
              <a href="#">feedback</a>.
            </div>
          </MessageBox>
        </div>
        <GenerateView />
      </main>
    </Layout>
  );
};

export const query = graphql`
  query HomePageQuery {
    site {
      siteMetadata {
        description
        title
      }
    }
  }
`;

export default IndexPage;
