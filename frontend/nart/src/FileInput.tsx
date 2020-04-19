
import React, { useMemo, useState, useEffect } from 'react';
import {useDropzone} from 'react-dropzone';

interface IProps {
    inputName: string;
    label: string;
    onSelected(file: any) : void;
    disabled?: boolean;
}

const baseStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderRadius: 2,
    borderColor: '#eeeeee',
    borderStyle: 'dashed',
    backgroundColor: '#fafafa',
    color: '#bdbdbd',
    outline: 'none',
    transition: 'border .24s ease-in-out',
    height: '100%'
};

const activeStyle = {
    borderColor: '#2196f3'
};

const acceptStyle = {
    borderColor: '#00e676'
};

const rejectStyle = {
    borderColor: '#ff1744'
};

const disabledStyle = {
    opacity: .5
}

export default function (props : IProps) { 

    let currentPreview : any = null;

    const onDroppedFile = (acceptedFiles : any) => {

        if (acceptedFiles.length > 0)
        {
            if (currentPreview)
                URL.revokeObjectURL(currentPreview);

            currentPreview = URL.createObjectURL(acceptedFiles[0]);
            setSelectedFile(Object.assign(acceptedFiles[0], { preview: currentPreview}));
        }
        else
            setSelectedFile(null);
    };
    
    const {
        getRootProps,
        getInputProps,
        isDragActive,
        isDragAccept,
        isDragReject
    } = useDropzone({
        accept: 'image/*',
        onDrop: onDroppedFile,
        disabled: props.disabled ?? false
    });

    const style : any = useMemo(() => ({
        ...baseStyle,
        ...(isDragActive ? activeStyle : {}),
        ...(isDragAccept ? acceptStyle : {}),
        ...(isDragReject ? rejectStyle : {}),
        ...(props.disabled ? disabledStyle : {})
    }), [
        isDragActive,
        isDragReject,
        props.disabled
    ]);

    const [selectedFile, setSelectedFile] = useState<any>(null);

    useEffect(() => {
        props.onSelected(selectedFile);
    }, [selectedFile]);

    return (
        <section className="container">
            <div {...getRootProps({style})}>
                <input {...getInputProps()} name={props.inputName} />
                <p>{props.label ?? "Drag 'n' drop some files here, or click to select files"}</p>
                {selectedFile ? <img className="thumbContainer" src={selectedFile?.preview} /> : null}
            </div>
        </section>
    );

};