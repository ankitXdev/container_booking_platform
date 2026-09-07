const RoleSelector = ({
  role,
  setRole,
}) => {
  return (
    <div className="role-selector">

      <button
        type="button"
        className={`role-card ${
          role === "exporter"
            ? "selected"
            : ""
        }`}
        onClick={() => setRole("exporter")}
      >

        <div className="role-icon">
          E
        </div>

        <div className="role-info">
          <h3>Exporter</h3>

          <p>
            Find and use container
            service providers.
          </p>
        </div>

        <div className="role-radio">
          {role === "exporter" && "✓"}
        </div>

      </button>

      <button
        type="button"
        className={`role-card ${
          role === "provider"
            ? "selected"
            : ""
        }`}
        onClick={() => setRole("provider")}
      >

        <div className="role-icon">
          P
        </div>

        <div className="role-info">
          <h3>Provider</h3>

          <p>
            Offer container services
            to exporters.
          </p>
        </div>

        <div className="role-radio">
          {role === "provider" && "✓"}
        </div>

      </button>

    </div>
  );
};

export default RoleSelector;