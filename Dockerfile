FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

# 1. Base, Locales y Pandoc
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
RUN apt-get update && apt-get install -y locales git curl wget ca-certificates \
    build-essential cmake libtool automake pkg-config software-properties-common \
    pandoc && \
    locale-gen en_US.UTF-8

#
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmbedtls-dev \
    libnng-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    git \
    cmake


# 2. R, Python y dependencias de sistema (Integrando NASA/Copernicus/Whitebox)
RUN apt-get update && apt-get install -y --no-install-recommends \
    r-base r-base-dev python3-pip python3-dev \
    psmisc lsof net-tools ffmpeg \
    libpng-dev libcairo2-dev libsystemd-dev \
    libfontconfig1-dev libfreetype6-dev \
    libharfbuzz-dev libfribidi-dev \
    libcurl4-openssl-dev libsqlite3-dev libxml2-dev libssl-dev \
    libgeos-dev libproj-dev libgdal-dev libudunits2-dev \
    libgit2-dev libssh2-1-dev libxt-dev libglpk-dev libmount-dev \
    libmagick++-dev libpcre2-dev libnetcdf-dev libhdf5-dev \
    libxt6 libxrender1 libxext6 default-jdk \
    && rm /usr/lib/python3.12/EXTERNALLY-MANAGED || true && \
    rm -rf /var/lib/apt/lists/*

# 3. Quarto CLI y TinyTeX (LaTeX para PDF)
RUN curl -LO https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.550/quarto-1.4.550-linux-amd64.deb \
    && dpkg -i quarto-1.4.550-linux-amd64.deb && rm quarto-1.4.550-linux-amd64.deb \
    && quarto install tinytex --no-prompt

# 4. Python Stack (Original + Nuevos)
RUN pip3 install --upgrade --ignore-installed --break-system-packages \
    # Ya estaban:
    shapely matplotlib numpy geopandas fiona pyyaml nbformat nbclient ipykernel \
    # Nuevos agregados:
    pandas rasterio rasterstats scipy psycopg2 pysal earthaccess cdsapi leafmap \
    geemap segment-geospatial geoai-py lidar pygis whitebox whiteboxgui streamlit \
    ghp-import jupyter-book jupyterlab jupytext mystmd notebook

# 5. R Stack (Original + Nuevos + Repos Especiales)
RUN R -e "options(timeout = 1000, Ncpus = parallel::detectCores(), repos = c(CRAN = 'https://packagemanager.posit.co/cran/__linux__/noble/latest')); \
    install.packages(c('ggplot2', 'patchwork', 'dplyr', 'remotes', 'languageserver', \
    'rmarkdown', 'units', 's2', 'sf', 'terra', 'stars', 'reticulate', 'IRkernel', \
    'unigd', 'cpp11', 'systemfonts', 'AsioHeaders', 'png', 'grid', 'JuliaCall', 'JuliaConnectoR', \
    # Nuevos CRAN:
    'tidyverse', 'tmap', 'leaflet', 'googleway', 'ggspatial', 'mapview', 'plotly', \
    'rasterVis', 'cartogram', 'geogrid', 'geofacet', 'linemap', 'tanaka', 'rayshader', \
    'lwgeom', 'gstat', 'spdep', 'spatialreg', 'stplanr', 'sfnetworks', 'spatstat', \
    'stpp', 'magrittr', 'giscoR', 'caret', 'tidymodels', 'spatialsample', 'CAST', \
    'mlr3spatial', 'mlr3spatiotempcv', 'ncdf4', 'whitebox'))"

# Starsdata y Repos Específicos (Con timeout extendido)
RUN R -e "options(timeout = 30000, Ncpus = parallel::detectCores()); \
    install.packages('starsdata', repos='https://cran.uni-muenster.de/pebesma/', type='source')" && \
    R -e "options(timeout = 2000, Ncpus = parallel::detectCores()); \
    install.packages(c('mlr3cmprsk', 'survdistr'), repos=c('https://mlr3learners.r-universe.dev', 'https://cloud.r-project.org')); \
    install.packages('geocompkg', repos=c('https://geocompr.r-universe.dev', 'https://cloud.r-project.org'), dependencies=TRUE); \
    whitebox::install_whitebox(); IRkernel::installspec(user = FALSE)"


#httpgd estable (v2.0.3)
RUN wget https://cran.r-project.org/src/contrib/Archive/httpgd/httpgd_2.0.3.tar.gz && \
    R CMD INSTALL httpgd_2.0.3.tar.gz && rm httpgd_2.0.3.tar.gz

# 6. Puente Python-R (Matplotlib Backend)
RUN mkdir -p /usr/local/lib/python3.12/dist-packages/reticulate/matplotlib && \
    touch /usr/local/lib/python3.12/dist-packages/reticulate/__init__.py

RUN printf 'def r_graphic_command(path):\n    import os\n    if os.path.exists(path): print(f"r_graphic_command: {path}")\n' > /usr/local/lib/python3.12/dist-packages/reticulate/__init__.py

RUN printf 'import matplotlib\nfrom matplotlib.backends.backend_agg import FigureCanvasAgg\nfrom matplotlib.backend_bases import FigureManagerBase\n\ndef show(*args, **kwargs):\n    import os, tempfile, reticulate\n    fd, path = tempfile.mkstemp(suffix=".png")\n    os.close(fd)\n    matplotlib.pyplot.savefig(path)\n    if hasattr(reticulate, "r_graphic_command"):\n        reticulate.r_graphic_command(path)\n\nclass FigureManager(FigureManagerBase):\n    def show(self):\n        show()\n\ndef new_figure_manager(num, *args, **kwargs):\n    FigureClass = kwargs.pop("FigureClass", matplotlib.figure.Figure)\n    thisFig = FigureClass(*args, **kwargs)\n    return new_figure_manager_given_figure(num, thisFig)\n\ndef new_figure_manager_given_figure(num, figure):\n    canvas = FigureCanvasAgg(figure)\n    manager = FigureManager(canvas, num)\n    return manager\n\nFigureCanvas = FigureCanvasAgg\n' > /usr/local/lib/python3.12/dist-packages/reticulate/matplotlib/backend.py

# 7. Julia: Instalación y Wrapper de Seguridad
ENV JULIA_VERSION=1.10.4
RUN wget https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-${JULIA_VERSION}-linux-x86_64.tar.gz \
    && tar -xvzf julia-${JULIA_VERSION}-linux-x86_64.tar.gz && mv julia-1.10.4 /opt/julia

# Wrapper para forzar LD_PRELOAD
RUN printf '#!/bin/bash\nexport LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libcurl.so.4:/usr/lib/x86_64-linux-gnu/libstdc++.so.6\nexport JULIA_PKG_USE_CLI_GIT=true\n/opt/julia/bin/julia "$@"\n' > /usr/local/bin/julia && chmod +x /usr/local/bin/julia
    
# 8. Julia: Configuración, Preferencias y Paquetes Core (Incluyendo Tables.jl)
RUN mkdir -p /root/.julia/environments/v1.10 && \
    printf "[LocalPreferences]\nGDAL_jll = { libgdal_path = \"/usr/lib/libgdal.so\" }\nGEOS_jll = { libgeos_path = \"/usr/lib/x86_64-linux-gnu/libgeos_c.so\" }\n" > /root/.julia/environments/v1.10/LocalPreferences.toml

# 9. Julia: Paquetes (Original + Nuevos)
RUN julia -e 'using Pkg; Pkg.add(["Preferences", "Suppressor", "RCall", "LibGEOS", "Tables", "DataFrames", "Plots", \
    "Statistics", "ArchGDAL", "LibPQ", "GeoDataFrames", "IJulia", "CSV", "CairoMakie", "AlgebraOfGraphics", \
    "DimensionalData", "FlexiJoins", "GeoFormatTypes", "GeoInterface", "GeoJSON", "GeoMakie", "GeometryOps", \
    "Makie", "MakieCore", "NaturalEarth", "Proj", "Rasters", "StatsBase", "Tyler", "GeoStats", "Graphs", \
    "NCDatasets", "MetaGraphsNext"])'

# Cirugía de Librerías (Sincronización de OpenSSL con el sistema Ubuntu Noble)
RUN find /root/.julia/artifacts -name "libssl.so*" -exec ln -sf /usr/lib/x86_64-linux-gnu/libssl.so.3 {} \; && \
    find /root/.julia/artifacts -name "libcrypto.so*" -exec ln -sf /usr/lib/x86_64-linux-gnu/libcrypto.so.3 {} \;

# Precompilación total: Esto garantiza que el arranque sea instantáneo en VSCode
RUN julia -e 'using Pkg; Pkg.precompile()'

# Y asegurar que en el runtime use los núcleos (ej. 8 núcleos)
ENV JULIA_NUM_THREADS=auto

# 10. CONFIGURACIÓN MAESTRA Rprofile.site (Build 47.42 - DPI/Ratio/Font/Reticulate-Hook)
RUN cat << 'EOF' > /usr/lib/R/etc/Rprofile.site
# --- 1. AJUSTES DE SISTEMA ---
Sys.setenv(JULIA_BINDIR = "/opt/julia/bin")
Sys.setenv(QUARTO_PYTHON = "/usr/bin/python3")

# Código Julia embebido (Auto-sanable)
.unal_julia_code <- '
using Suppressor, Plots, Statistics
function _unal_core_executor(code, is_plot, filename, dpi, w, h, fs)
    @capture_out begin
        if is_plot
            default(dpi=dpi, size=(w, h), titlefontsize=fs+2, 
                    guidefontsize=fs, tickfontsize=fs-2, legendfontsize=fs-1)
        end
        pos = 1
        while pos <= lastindex(code)
            start_idx = pos
            try
                ex, pos = Meta.parse(code, pos)
                cmd_part = strip(code[start_idx:prevind(code, pos)])
                if !isempty(cmd_part)
                    println("julia> ", cmd_part)
                    res = eval(ex)
                    if res !== nothing && !(res isa Plots.Plot)
                        show(stdout, MIME("text/plain"), res)
                        println()
                    end
                    println() 
                end
            catch e
                println("julia> Error: ", e)
                break
            end
        end
        if is_plot && current() !== nothing; savefig(current(), filename); end
    end
end
'

.ensure_julia_ready <- function() {
  if (!requireNamespace("JuliaConnectoR", quietly = TRUE)) stop("JuliaConnectoR missing")
  if (!JuliaConnectoR::juliaEval('isdefined(Main, :_unal_core_executor)')) {
    JuliaConnectoR::juliaEval(.unal_julia_code)
  }
}

j_eval <- function(cmd) {
  .ensure_julia_ready()
  cat(JuliaConnectoR::juliaCall("_unal_core_executor", cmd, FALSE, "", 72, 800, 500, 12))
}

j_plot <- function(cmd, n = "tmp_plot.png", dpi = 300, w = 800, h = NULL, ratio = 1.6, fontsize = 12) {
  .ensure_julia_ready()
  if (is.null(h)) h <- round(w / ratio)
  log_out <- JuliaConnectoR::juliaCall("_unal_core_executor", cmd, TRUE, n, dpi, as.integer(w), as.integer(h), as.integer(fontsize))
  if (nchar(log_out) > 0) cat(log_out)
  if (file.exists(n)) {
    img <- png::readPNG(n)
    grid::grid.newpage()
    grid::grid.raster(img)
  }
}

# --- 2. CARGA DE LIBRERÍAS Y INTERFAZ ---
library(png)
library(grid)

if (interactive()) {
  # Visor httpgd para VSCode
  if (requireNamespace("httpgd", quietly = TRUE)) {
    options(device = "httpgd", httpgd.host = "0.0.0.0", httpgd.port = 8787, httpgd.token = FALSE)
  }
  
  # Hook para que Matplotlib (Python) use el visor de R
  setHook(packageEvent("reticulate", "onLoad"), function(...) {
    try({
      ret_py <- reticulate::import("reticulate", delay_load = TRUE)
      reticulate::py_set_attr(ret_py, "r_graphic_command", function(path) {
        if (file.exists(path)) {
          img <- png::readPNG(path); grid::grid.newpage(); grid::grid.raster(img)
        }
      })
      reticulate::py_run_string("import matplotlib; matplotlib.use('module://reticulate.matplotlib.backend')")
    }, silent = TRUE)
  })
}
EOF

# Duplicamos el Rprofile para asegurar compatibilidad con todas las versiones de R en Ubuntu
#RUN cp /usr/lib/R/etc/Rprofile.site /etc/R/Rprofile.site


# 10. Finalización
WORKDIR /home/rstudio/work
RUN chmod -R 777 /home/rstudio/work

EXPOSE 8888
EXPOSE 8787
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token='geomatica2025'"]
