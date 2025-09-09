mkdi -p ~/.streamlit/
echo "\
post = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\"> ~/.streamlit/config.toml