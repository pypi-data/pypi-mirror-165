import { SwatchIcon } from "@heroicons/react/24/outline";
import * as React from "react";
import { SectionHeader } from "../../atoms";
import Icon from "../../icons";
import { IPromptConfig } from "../../types";
import { loadJSONData } from "../../utils";
import GeneratorControlsView from "./controls";
import GeneratorControls from "./controls";
import GalleryView from "./gallery";

const GenerateView = ({ data }: any) => {
  const initConfig: IPromptConfig = {
    prompt: "",
    num_images: 6,
    guidance_scale: 7.5,
    num_inference_steps: 50,
    height: 512,
    width: 512,
  };
  const serverUrl = process.env.GATSBY_API_URL;
  const [loading, setLoading] = React.useState(false);
  const [results, setResults] = React.useState<null | {}>(null);
  const [generationConfig, setGenerationConfig] = React.useState(initConfig);

  const [prompt, setPrompt] = React.useState<string>(
    "portrait of leprechaun, intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha, 8 k "
  );

  const updateConfig = (config: IPromptConfig) => {
    setGenerationConfig(config);
  };

  const fetchGeneration = (prompt: string | undefined) => {
    if (prompt) {
      const config = { ...generationConfig, prompt };
      console.log("fetching generation", config);
      setResults({});
      const resultsUrl = `${serverUrl}/generate`;
      const postData = {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...generationConfig, prompt }),
      };
      setLoading(true);
      loadJSONData(resultsUrl, postData)
        .then((data) => {
          setLoading(false);
          if (data && data.status) {
            console.log("data", data);
            setResults(data);
          }
        })
        .catch((err) => {
          console.log("err", err);
          setResults({});
          setLoading(false);
        });
    }
  };

  const promptInputRef = React.useRef<HTMLInputElement>(null);
  return (
    <div className="mpb-4 pb-4">
      <SectionHeader
        icon={
          <SwatchIcon className="inline-block h-7 text-indigo-600 -mt-1 mr-1" />
        }
        title={"Generate"}
      ></SectionHeader>
      {/* {loading && <LoadBox subtitle={"fetching generation"} />} */}

      <>
        <GeneratorControlsView
          setConfig={updateConfig}
          config={generationConfig}
        />
      </>
      <>
        <div className="border border-gray-50 p-3 rounded flex shadow-lg">
          <input
            className="w-full p-3 text-gray-500 rounded border border-gray-200 inline-block rounded-r-none"
            placeholder="Enter trackingId"
            type={"text"}
            defaultValue={prompt}
            ref={promptInputRef}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                // fetchGeneration(promptInputRef.current?.value);
                fetchGeneration(promptInputRef.current?.value);
              }
            }}
          />
          <div
            role={"button"}
            className={`border p-3 px-5 rounded bg-indigo-500 cursor-pointer hover:bg-indigo-700 transition duration-500 text-lg rounded-l-none text-white ${
              loading ? " opacity-90 pointer-events-none disabled " : ""
            }`}
            onClick={(e) => {
              // setSearchResults(dummyData)
              const currentPrompt = promptInputRef.current!.value;
              setPrompt(currentPrompt);
              // fetchResults(currentPrompt);
              fetchGeneration(currentPrompt);
            }}
          >
            <div className="inline-block ">
              {loading && <Icon size={5} icon="loading" />}
              {!loading && <span className="inline-block">Generate</span>}
            </div>{" "}
          </div>
        </div>
      </>

      {results && (
        <div className="  mt-6 rounded ">
          <div className="text-xs text-gray-500 py-2"> Generated Images</div>
          <GalleryView data={results} />
        </div>
      )}
    </div>
  );
};
export default GenerateView;
