# ==============================================================================
# MOTOR DE INTEROPERABILIDAD GEOMÁTICA (UNAL) - VERSIÓN PRO (NIVEL MAESTRÍA)
# ==============================================================================

.j_render_output <- function(res_raw) {
  fmt_html <- FALSE; fmt_pdf <- FALSE
  if ("knitr" %in% loadedNamespaces()) {
    out_fmt <- knitr::opts_knit$get("out.format")
    if (!is.null(out_fmt)) {
      if (out_fmt %in% c("html", "markdown", "quarto")) fmt_html <- TRUE
      if (out_fmt %in% c("latex", "pdf")) fmt_pdf <- TRUE
    }
  }

  safe_escape <- function(x) {
    x <- gsub("&", "&amp;", x, fixed = TRUE)
    x <- gsub("<", "&lt;", x, fixed = TRUE)
    x <- gsub(">", "&gt;", x, fixed = TRUE)
    return(x)
  }

  res_l <- gsub("\033\\[[0-9;]*m", "", res_raw)
  partes <- strsplit(res_l, "\n")[[1]]
  
  # Inicialización estricta
  out_triple <- 0; out_comentario <- 0; out_comillas <- 0; out_bloque <- 0
  current_mode <- "none" 

  if (fmt_pdf) cat("\\begin{verbatim}\n")

  for (p in partes) {
    is_prompt <- grepl("^julia> ", p)
    is_code <- is_prompt || (out_triple > 0) || (out_comentario > 0) || (out_bloque > 0) || (out_comillas > 0)
    
    if (is_code) {
      p_clean <- if (is_prompt) sub("^julia> ", "", p) else p
      
      n_triples <- lengths(regmatches(p_clean, gregexpr('"""', p_clean, fixed = TRUE)))
      if (n_triples > 0) out_triple <- (out_triple + n_triples) %% 2
      
      n_abre <- lengths(regmatches(p_clean, gregexpr("#=", p_clean, fixed = TRUE)))
      n_cierra <- lengths(regmatches(p_clean, gregexpr("=#", p_clean, fixed = TRUE)))
      if (n_abre > 0 || n_cierra > 0) out_comentario <- out_comentario + n_abre - n_cierra
      
      if (out_triple == 0 && out_comentario <= 0) {
        # Limpieza para no confundir el parser
        p_ev <- gsub('"""', '', p_clean, fixed = TRUE)
        p_ev <- gsub('"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', '""', p_ev, perl = TRUE)
        p_ev <- gsub("'[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", "''", p_ev, perl = TRUE)
        p_ev <- sub("#.*", "", p_ev) 
        
        n_comillas <- lengths(regmatches(p_ev, gregexpr('"', p_ev, fixed = TRUE)))
        if (n_comillas > 0) out_comillas <- (out_comillas + n_comillas) %% 2
        
        if (out_comillas == 0) {
          # FIX PRO: Contar apariciones exactas, no solo presencias (grepl)
          patron_abrir <- "\\b(do|function|for|if|begin|let|while|macro|try|module|baremodule|struct|quote)\\b"
          abrir_out <- lengths(regmatches(p_ev, gregexpr(patron_abrir, p_ev))) + 
                       lengths(regmatches(p_ev, gregexpr("(", p_ev, fixed = TRUE))) + 
                       lengths(regmatches(p_ev, gregexpr("[", p_ev, fixed = TRUE)))
          
          cerrar_out <- lengths(regmatches(p_ev, gregexpr("\\bend\\b", p_ev))) + 
                        lengths(regmatches(p_ev, gregexpr(")", p_ev, fixed = TRUE))) + 
                        lengths(regmatches(p_ev, gregexpr("]", p_ev, fixed = TRUE)))
                        
          out_bloque <- out_bloque + abrir_out - cerrar_out
        }
      }
      
      if (fmt_html) {
        if (current_mode != "code") {
          if (current_mode == "data") cat("</pre>\n")
          cat("<pre class='julia-code' style='display:block; background:#f4f6f8; border:1px solid #c0c8d0; border-radius:4px; padding:10px; margin-top:10px; margin-bottom:0; font-family:\"Lucida Console\", Consolas, monospace; font-size:0.9em; white-space:pre-wrap; color:#333;'>\n")
          current_mode <- "code"
        }
        p_html <- if (is_prompt) "<span style='color:#28a745; font-weight:bold;'>julia&gt; </span>" else "       "
        cat(paste0(p_html, "<span style='color:#008b8b;'>", safe_escape(p_clean), "</span>\n"))
      } else if (!fmt_pdf) {
        p_cons <- if (is_prompt) "\033[32mjulia> \033[0m" else "       "
        cat(paste0(p_cons, "\033[36m", p_clean, "\033[0m\n"))
      } else { cat(paste0(if(is_prompt) "julia> " else "       ", p_clean, "\n")) }
      
    } else {
      if (fmt_html) {
        if (current_mode != "data") {
          if (current_mode == "code") cat("</pre>\n")
          cat("<pre class='julia-output' style='display:block; background:#ffffff; border:none; padding:10px 10px 10px 20px; margin-top:0; margin-bottom:15px; font-family:\"Lucida Console\", Consolas, monospace; font-size:0.9em; white-space:pre-wrap; color:#000;'>\n")
          current_mode <- "data"
        }
        cat(paste0(safe_escape(p), "\n"))
      } else { cat(paste0(p, "\n")) }
    }
  }
  if (fmt_html && current_mode != "none") cat("</pre>\n")
  else if (fmt_pdf) cat("\\end{verbatim}\n\n")
}

j_eval <- function(cmd) {
  .ensure_julia_ready()
  lineas <- strsplit(cmd, "\n")[[1]]
  buffer <- ""; en_bloque <- 0; en_comillas <- 0; en_comentario_multi <- 0; en_triple_comilla <- 0
  resultado_final <- NULL

  for (l in lineas) {
    if (trimws(l) == "" && en_comentario_multi == 0 && en_triple_comilla == 0 && en_comillas == 0 && en_bloque == 0) next
    buffer <- paste0(buffer, l, "\n")
    
    num_triples <- lengths(regmatches(l, gregexpr('"""', l, fixed = TRUE)))
    if (num_triples > 0) en_triple_comilla <- (en_triple_comilla + num_triples) %% 2
    
    num_com_abre <- lengths(regmatches(l, gregexpr("#=", l, fixed = TRUE)))
    num_com_cierra <- lengths(regmatches(l, gregexpr("=#", l, fixed = TRUE)))
    if (num_com_abre > 0 || num_com_cierra > 0) en_comentario_multi <- en_comentario_multi + num_com_abre - num_com_cierra
    
    if (en_triple_comilla == 0 && en_comentario_multi <= 0) {
      l_clean <- gsub('"""', '', l, fixed = TRUE)
      l_clean <- gsub('"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', '""', l_clean, perl = TRUE)
      l_clean <- gsub("'[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", "''", l_clean, perl = TRUE)
      l_clean <- sub("#.*", "", l_clean)
      
      num_comillas <- lengths(regmatches(l_clean, gregexpr('"', l_clean, fixed = TRUE)))
      if (num_comillas > 0) en_comillas <- (en_comillas + num_comillas) %% 2
      
      if (en_comillas == 0) {
        patron_abrir <- "\\b(do|function|for|if|begin|let|while|macro|try|module|baremodule|struct|quote)\\b"
        abrir <- lengths(regmatches(l_clean, gregexpr(patron_abrir, l_clean))) + 
                 lengths(regmatches(l_clean, gregexpr("(", l_clean, fixed = TRUE))) + 
                 lengths(regmatches(l_clean, gregexpr("[", l_clean, fixed = TRUE)))
                 
        cerrar <- lengths(regmatches(l_clean, gregexpr("\\bend\\b", l_clean))) + 
                  lengths(regmatches(l_clean, gregexpr(")", l_clean, fixed = TRUE))) + 
                  lengths(regmatches(l_clean, gregexpr("]", l_clean, fixed = TRUE)))
                  
        en_bloque <- en_bloque + abrir - cerrar
      }
    }
    
    if (en_bloque <= 0 && en_comillas == 0 && en_comentario_multi <= 0 && en_triple_comilla == 0) {
      res_raw <- JuliaConnectoR::juliaCall("_unal_core_executor", buffer, FALSE, "", 72, 800, 500, 12)
      .j_render_output(res_raw)
      
      res_l <- gsub("\033\\[[0-9;]*m", "", res_raw)
      lineas_res <- strsplit(res_l, "\n")[[1]]
      lineas_res <- trimws(lineas_res[lineas_res != ""])
      temp_res <- tail(lineas_res[!grepl("^julia>", lineas_res)], 1)
      if (length(temp_res) > 0) resultado_final <- temp_res
      
      # Reset seguro del buffer
      buffer <- ""; en_bloque <- 0; en_comillas <- 0; en_comentario_multi <- 0; en_triple_comilla <- 0
    }
  }
  return(invisible(resultado_final))
}

j_plot <- function(cmd, n = "tmp_plot.png", dpi = 300, w = 800, h = NULL, ratio = 1.6, fontsize = 12) {
  .ensure_julia_ready()
  if (is.null(h)) h <- round(w / ratio)
  
  lineas <- strsplit(cmd, "\n")[[1]]
  buffer <- ""; en_bloque <- 0; en_comillas <- 0; en_comentario_multi <- 0; en_triple_comilla <- 0
  
  for (l in lineas) {
    if (trimws(l) == "" && en_comentario_multi == 0 && en_triple_comilla == 0 && en_comillas == 0 && en_bloque == 0) next
    buffer <- paste0(buffer, l, "\n")
    
    num_triples <- lengths(regmatches(l, gregexpr('"""', l, fixed = TRUE)))
    if (num_triples > 0) en_triple_comilla <- (en_triple_comilla + num_triples) %% 2
    
    num_com_abre <- lengths(regmatches(l, gregexpr("#=", l, fixed = TRUE)))
    num_com_cierra <- lengths(regmatches(l, gregexpr("=#", l, fixed = TRUE)))
    if (num_com_abre > 0 || num_com_cierra > 0) en_comentario_multi <- en_comentario_multi + num_com_abre - num_com_cierra
    
    if (en_triple_comilla == 0 && en_comentario_multi <= 0) {
      l_clean <- gsub('"""', '', l, fixed = TRUE)
      l_clean <- gsub('"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', '""', l_clean, perl = TRUE)
      l_clean <- gsub("'[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", "''", l_clean, perl = TRUE)
      l_clean <- sub("#.*", "", l_clean)
      
      num_comillas <- lengths(regmatches(l_clean, gregexpr('"', l_clean, fixed = TRUE)))
      if (num_comillas > 0) en_comillas <- (en_comillas + num_comillas) %% 2
      
      if (en_comillas == 0) {
        patron_abrir <- "\\b(do|function|for|if|begin|let|while|macro|try|module|baremodule|struct|quote)\\b"
        abrir <- lengths(regmatches(l_clean, gregexpr(patron_abrir, l_clean))) + 
                 lengths(regmatches(l_clean, gregexpr("(", l_clean, fixed = TRUE))) + 
                 lengths(regmatches(l_clean, gregexpr("[", l_clean, fixed = TRUE)))
                 
        cerrar <- lengths(regmatches(l_clean, gregexpr("\\bend\\b", l_clean))) + 
                  lengths(regmatches(l_clean, gregexpr(")", l_clean, fixed = TRUE))) + 
                  lengths(regmatches(l_clean, gregexpr("]", l_clean, fixed = TRUE)))
                  
        en_bloque <- en_bloque + abrir - cerrar
      }
    }
    
    if (en_bloque <= 0 && en_comillas == 0 && en_comentario_multi <= 0 && en_triple_comilla == 0) {
      res_log <- JuliaConnectoR::juliaCall("_unal_core_executor", buffer, TRUE, n, dpi, as.integer(w), as.integer(h), as.integer(fontsize))
      .j_render_output(res_log)
      buffer <- "" 
    }
  }
  
  if (file.exists(n)) {
    img <- png::readPNG(n)
    grid::grid.newpage(); grid::grid.raster(img)
  }
}