import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { requestAPI } from '../../handler';
import { Nullable, AnyObject } from 'tsdef';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowTestRunPanel {
  className?: string;
  workflowName: string;
  workflowDefaults: AnyObject;
  workflowDemoData: AnyObject;
}

const WorkflowTestRunPanel = ({
  className,
  workflowName,
  workflowDefaults,
  workflowDemoData
}: IWorkflowTestRunPanel): JSX.Element => {
  // ------------------------------------
  // Initialise state
  // ------------------------------------
  const navigate = useNavigate();

  // Parameters
  const [instParams] = useState<AnyObject>({
    ...workflowDefaults,
    ...workflowDemoData
  });

  // Instance Create
  const [instCreateError, setInstCreateError] = useState<Nullable<string>>();

  // ------------------------------------
  // Handle workflow launch
  // ------------------------------------
  const launchWorkflow = async () => {
    const { created, instance, error } = await requestAPI<any>('instances', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        workflow: workflowName,
        params: instParams,
        name: `test-${workflowName}`
      })
    });
    if (error) {
      setInstCreateError(error);
    }
    if (!created) {
      return;
    }
    navigate(`/instances/${instance.id}`);
  };

  return (
    <div className={`launch-panel ${className}`}>
      {/* Instance name */}
      <div className="test-run-intro">
        <div>
          <div className="test-run-intro-header">
            <h3>Running {workflowName} with test data</h3>
          </div>
          <p>
            This mode will perform a test run of the workflow using freely
            provided demo data. This is a great way to interactively examine the
            report and outputs that the workflow generates in order to determine
            if that information will be useful in your analysis.
          </p>
          <span className="divider" />
          <p>
            Please note: The demo data may need to be downloaded during the
            running of the application, so if your internet connection is
            interrupted during this process the workflow may fail.
          </p>
        </div>
      </div>

      {/* Workflow launch */}
      <div className={'launch-control active'}>
        <button onClick={() => launchWorkflow()}>Launch Workflow</button>
        {instCreateError ? (
          <div className="error">
            <p>Error: {instCreateError}</p>
          </div>
        ) : (
          ''
        )}
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowTestRunPanel = styled(WorkflowTestRunPanel)`
  && {
    max-width: 1024px;
    padding: 0 0 15px 0;
    margin: 0 auto;
  }

  //
  // Information panel
  //
  .test-run-intro {
    border-radius: 4px;
    padding: 25px;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .test-run-intro-header {
    padding-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .divider {
    height: 1px;
    width: 100%;
    margin: 15px 0;
    display: flex;
    background-color: #f2f2f2;
  }

  //
  // Launch control
  //
  .launch-control {
    margin: 15px 0 0 0;
  }

  .launch-control button {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px;
    border: 0;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    cursor: pointer;
  }

  .launch-control.active button {
    border: 1px solid #1d9655;
    background-color: #1d9655;
    color: white;
  }
  .launch-control.active button:hover {
    cursor: pointer;
    background-color: white;
    color: #1d9655;
  }
  .launch-control.error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledWorkflowTestRunPanel;
