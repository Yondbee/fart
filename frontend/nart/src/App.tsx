import React, {useState, useEffect} from 'react';

import './App.css';

import FileInput from './FileInput';



function App() {

  const [currentMsg, setCurrentMsg] = useState('⬆ Drag two images above to start ⬆');
  const [isLoading, setLoading] = useState(false);
  const [leftImage, setLeftImage] = useState();
  const [rightImage, setRightImage] = useState();
  const [resultImage, setResultImage] = useState<string>();

  const processImage = async () => {
    let data = new FormData();
    
    // @ts-ignore
    data.append('src', leftImage);

    // @ts-ignore
    data.append('sty', rightImage);
        
    try {
      const result = await fetch('http://34.89.112.32/fartist', {
        method: 'POST',
        body: data
      })

      setResultImage(URL.createObjectURL(await result.blob()));
      setLoading(false);
    }
    catch (e)
    {
      setCurrentMsg('Error, please try again');
      setLoading(false);
    }
  }  

  useEffect(() => {

    console.log(leftImage, 'leftImage');
    console.log(rightImage, 'rightImage');

    if (leftImage && rightImage && !isLoading)
    {
      setLoading(true);
      setCurrentMsg('Processing, this might take up to 30 seconds...')
      
      processImage();
    }

  }, [leftImage, rightImage]);

  return (
    <div className="App">
      <header className="App-header">
        <h2>
          YONDBEE Art Mixer
        </h2>
        Like it? <a
          className="App-link"
          href="mailto:info@yondbee.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          Get in touch
        </a>
      </header>
      <main>
        <form method='post' action=''>
          <section className="Main-Grid">
            <div className="left">
              <FileInput inputName='src' label="Drag source file here" onSelected={(file) => setLeftImage(file)} disabled={isLoading}/>
            </div>          
            <div className="right">
              <FileInput inputName='sty' label="Drag style reference file here" onSelected={(file) => setRightImage(file)} disabled={isLoading} />
            </div>
            <div className="bottom">
              {resultImage ? 
                <img src={resultImage} className='thumbContainer'/>
                : <code>{currentMsg}</code>}
            </div>
          </section>
        </form>
      </main>
      <footer className="App-footer">
        <code>Based on <a href="https://www.tensorflow.org/tutorials/generative/style_transfer">NST</a>, hacked by <a href="mailto:andrea@yondbee.com">Andrea</a>.</code>
      </footer>
    </div>
  );
}

export default App;
